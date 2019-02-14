import os
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re

from scrap.tools import debug_print
from scrap.tools import parse_url_to_postForm
from scrap.tools import make_dir
from urllib.parse import urlencode
from urllib.request import Request


def download_file(path, root_url, data_url, download_url, option='urlopen'):
    make_dir(path)
    total_url = root_url + data_url
    if option == 'urlopen' :
        with urlopen(total_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html5lib')
    elif option == 'post':
        total_url, post_fields = parse_url_to_postForm(total_url)
        request = Request(total_url, urlencode(post_fields).encode())
        json = urlopen(request).read().decode()
        soup = BeautifulSoup(json, 'html5lib')
    tag_as = soup.find_all("a")
    if not tag_as == None:
        for idx2, tag_a in enumerate(tag_as):
            if not tag_a.get('href') == None:
                for key, value in download_url.items():
                    if key in tag_a.get('href'):
                        #necessary_word, root_url, download_url, tag_a, path
                        download_item(necessary_word=key, root_url=root_url, download_url=value, tag_a=tag_a, path=path)

def download_file_g2bDetail(path, root_url, data_url, download_url, necessary_words=[], option='urlopen'):
    make_dir(path)
    total_url = root_url + data_url
    if option == 'urlopen' :
        with urlopen(total_url) as response:
            html = response.read().decode('CP949', errors='ignore')
            soup = BeautifulSoup(html, 'html5lib')
    elif option == 'post':
        total_url, post_fields = parse_url_to_postForm(total_url)
        request = Request(total_url, urlencode(post_fields).encode())
        json = urlopen(request).read().decode()
        soup = BeautifulSoup(json, 'html5lib')
    bodyUrl = soup.find('iframe').get('src')
    if not bodyUrl == None:
        if option == 'urlopen':
            with urlopen(bodyUrl) as response:
                html = response.read().decode('CP949', errors='ignore')
                soup = BeautifulSoup(html, 'html5lib')
        elif option == 'post':
            total_url, post_fields = parse_url_to_postForm(total_url)
            request = Request(total_url, urlencode(post_fields).encode())
            json = urlopen(request).read().decode()
            soup = BeautifulSoup(json, 'html5lib')

    tag_as = soup.find_all('a')
    if not tag_as == None:
        for idx2, tag_a in enumerate(tag_as):
            if not tag_a.get('href') == None:
                for key, value in download_url.items():
                    if key in tag_a.get('href'):
                        #necessary_word, root_url, download_url, tag_a, path
                        download_item(necessary_word=key, root_url=root_url, download_url=value, tag_a=tag_a, path=path)

def download_item(necessary_word, root_url, download_url, tag_a, path):
    if necessary_word == 'downloadAttachFile':
        if not tag_a.get('href') == None:
            file_number = re.sub("[^0-9]", "", tag_a.get('href'))
            file_name = tag_a.get_text()
            file_download_url = root_url + download_url + file_number
            save_file_path = os.path.join(path, file_name)
            if not os.path.isfile(save_file_path):
                print("NO FILE", save_file_path)
                urlretrieve(file_download_url, save_file_path)
    elif necessary_word == 'attachDown':
        if not tag_a.get('href') == None:
            file_number = re.sub("[^0-9]", "", tag_a.get('href'))
            file_name = tag_a.get_text()
            file_download_url = root_url + download_url + file_number
            save_file_path = os.path.join(path, file_name)
            if not os.path.isfile(save_file_path):
                print("NO FILE", save_file_path)
                urlretrieve(file_download_url, save_file_path)
    elif necessary_word == '#':
        if not tag_a.get('fileseq') == None:
            file_number = re.sub("[^0-9]", "", tag_a.get('fileseq'))
            file_name = tag_a.get('title')
            file_download_url = root_url + download_url + file_number
            save_file_path = os.path.join(path, file_name)
            if not os.path.isfile(save_file_path):
                print("NO FILE", save_file_path)
                urlretrieve(file_download_url, save_file_path)
    elif necessary_word == 'toFileDownload':
        if not tag_a.get('href') == None:
            file_number = tag_a.get('href').split("(")[1].split(")")[0].split("'")[1]
            file_name = tag_a.get_text()
            file_name = re.sub('[?,!/;:<>]', '', file_name)
            file_download_url = root_url + download_url + file_number
            save_file_path = os.path.join(path, file_name)
            if not os.path.isfile(save_file_path):
                print("NO FILE", save_file_path)
                urlretrieve(file_download_url, save_file_path)
    elif necessary_word == 'eeOrderAttachFileDownload':
        if not tag_a.get('href') == None:
            file_number = tag_a.get('href').split("(")[1].split(")")[0].split("'")[3]
            file_option = '&fileSn=' + tag_a.get('href').split("(")[1].split(")")[0].split("'")[5]
            file_name = tag_a.get_text()
            file_name = re.sub('[?,!/;:<>]', '', file_name)
            file_download_url = root_url + download_url + file_number + file_option
            save_file_path = os.path.join(path, file_name)
            if not os.path.isfile(save_file_path):
                print("NO FILE", save_file_path)
                urlretrieve(file_download_url, save_file_path)



