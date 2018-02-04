 # -*- coding: utf-8 -*-

import csv
import requests
from bs4 import BeautifulSoup


def get_categories_urls():
    '''
    Ссылки на все категории.
    '''
    page = requests.get('https://www.goodfon.ru/')
    soup = BeautifulSoup(page.text, 'html.parser')
    categories_html = soup.find(class_='featuree').find_all(class_='menu')
    return [category['href'] for category in categories_html]


def get_page_count(url):
    '''
    Количество страниц в одной категории.
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return int(soup.find(class_='pageinfo').find('div').contents[0])


def get_images_data(category_url, offset=1, max_pages=10):
    '''
    Список ссылок и тегов на картинки из определённой категории.
    '''
    pages_numbers = range(offset, max_pages + 1)
    pages_urls = [category_url + 'index-{}.html'.format(i) for i in pages_numbers]
    links = []
    tags = []
    for url in pages_urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        img_list = soup.find_all(class_='tabl_td')
        links += [img.find('a')['href'] for img in img_list]
        tags += [img.find('a')['title'] for img in img_list]
    return links, tags

def get_original_link(image_url, page=None):
    if not page:
        page = requests.get(image_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    b = soup.find_all('b')
    for tag in b:
        if tag.parent.find('a'):
            link = tag.parent.find('a')['href']
        if link[:10] == '/download/':
            url = 'https://www.goodfon.ru' + link
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find('small').parent.find('a')['href']

# Если нужны все категории
# categories = get_categories_urls()

# Только определённые категории
categories = ['girls', 'space', 'cats', 'minimalism', 'landscapes', 'nature']

for category in categories:
    url = 'https://www.goodfon.ru/catalog/{}/'.format(category)
    f = csv.writer(open(category + '.csv', 'w'))
    f.writerow(['Категория', 'Сслыка на странцу', 'Теги', 'Ссылка на оригинал'])
    img_links, img_tags = get_images_data(url)
    for link, tags in zip(img_links, img_tags):
        category = url[31:-1]
        original_link = get_original_link(link)
        f.writerow([category, link, tags, original_link])
        print([category, link, tags, original_link])
