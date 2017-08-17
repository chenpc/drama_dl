# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import codecs
import sys
import os
import subprocess
from multiprocessing import Pool

url = 'http://www.drama01.com'




def exec_command(cmd, timeout=None):
    res = subprocess.run(cmd, shell=True, timeout=timeout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res.stdout = res.stdout.decode('utf-8')
    res.stderr = res.stderr.decode('utf-8')
    return res


def get_drama_list(type="jp"):
    d = pq(url=url+"/"+type)
    ul = d('#nav > div:nth-child(5) > ul')
    div = ul.find('li > h4 > a').items()

    drama_list = list()
    for d in div:
        drama_list.append(url+d.attr('href'))

    return drama_list


def download_ep(title_ep_url):
    title = title_ep_url[0]
    ep_url = title_ep_url[1]
    d = pq(url=ep_url)
    dm = d('#main > div > a')
    video_url = dm.attr('href')
    filename = exec_command('youtube-dl -e %s' % video_url).stdout
    output_name = os.path.join(title, filename).strip()
    if video_url is None:
        return
    try:
        os.mkdir(title)
    except:
        pass
    print("output_name", output_name)
    os.system('youtube-dl --socket-timeout 30 %s -o "%s.mp4"' % (video_url, output_name))


def download_dramas(drama_url):
    result = list()
    d = pq(url=drama_url)


    try:
        title = d('#main > div.item-page > h1').text().encode('iso-8859-1')
        title = codecs.decode(title, 'utf-8')
    except:
        return

    ep_list = d('#top > ul > li > a').items()
    for ep in ep_list:
        try:
            href = ep.attr('href')
            result.append((title, drama_url + href))
            # download_ep(title, drama_url + href)
        except:
            pass
    return result



if __name__ == "__main__":
    pool = Pool(processes=32)
    if len(sys.argv) != 2:
        sys.exit()

    type = sys.argv[1]
    drama_list = get_drama_list(type)
    # pool.map(download_dramas, drama_list)
    all_eps = list()
    for drama in drama_list:
        eps = download_dramas(drama)
        if eps:
            all_eps = all_eps + eps


    pool.map(download_ep, all_eps)



