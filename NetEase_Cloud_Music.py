import os
import re

import requests

head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
}

url = 'https://music.163.com/discover/toplist'
response = requests.get(url=url, headers=head)
response.encoding = response.apparent_encoding
a = response.text
html_data = re.findall(
    '<a href="/discover/toplist\?id=(.*?)" class="s-fc0">(.*?)</a>', a)
for list_id in html_data:
    ls_id = list_id[0]
    ls_name = list_id[1]

    HOT_url = f'https://music.163.com/discover/toplist?id={ls_id}'
    resp = requests.get(url=HOT_url, headers=head)
    b = resp.text
    HT_data = re.findall('<li><a href="/song\?id=(.*?)">(.*?)</a>', b)
    HT_date = re.findall('<span class="sep s-fc3">最近更新：(.*?)</span>', b)
    date = HT_date[0]
    filename = f'D:/NetEase_Cloud_Music/{ls_name}_{date}/'
    if not os.path.exists(filename):
        os.mkdir(filename)
    for info in HT_data:
        music_id = info[0]
        music_name = info[1]
        music_name = re.sub('[\\/:*?,.\"<>|\\n\']', '', music_name)
        music_url = f"https://music.163.com/song/media/outer/url?id={music_id}"
        music_content = requests.get(url=music_url, headers=head).content
        with open(filename+music_name+'.mp3', mode='wb')as f:
            f.write(music_content)
        print(ls_name, music_name)
    print(ls_name+"Downloading!!!!!")
