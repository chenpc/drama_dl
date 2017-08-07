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


def get_drama_list():
    d = pq(url=url+"/jp")
    div = d('#nav > div:nth-child(7) > ul').find('li > h4 > a').items()

    drama_list = list()
    for d in div:
        drama_list.append(url+d.attr('href'))

    return drama_list


def download_ep(title, ep_url):
    d = pq(url=ep_url)
    dm = d('#main > div > a')
    video_url = dm.attr('href')
    try:
        os.mkdir(title)
    except:
        pass
    filename = exec_command('youtube-dl -e %s' % video_url).stdout
    output_name = os.path.join(title, filename).strip()
    print("output_name", output_name)
    os.system('youtube-dl --socket-timeout 30 %s -o "%s.mp4"' % (video_url, output_name))


def download_dramas(drama_url):
    d = pq(url=drama_url)

    try:
        title = d('#main > div.item-page > h1').text().encode('iso-8859-1')
        title = codecs.decode(title, 'utf-8')
    except:
        return

    ep_list = d('#top > ul > li > a').items()
    for ep in ep_list:
        download_ep(title, drama_url+ep.attr('href'))


if __name__ == "__main__":
    pool = Pool(processes=32)
    drama_list = get_drama_list()
    pool.map(download_dramas, drama_list)


