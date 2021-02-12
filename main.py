import requests
from bs4 import BeautifulSoup as bs 
from datetime import datetime 
from pprint import pprint

from random import choice

import logging

from fake_useragent import UserAgent


def get_content(url, proxy=None):
	ua = UserAgent()
	user_agent ={'User-Agent': ua.random}
	proxy = {'http': 'http://'+ choice(proxy)}
	try:
		content = requests.get(url, headers=user_agent, proxies=proxy)
		return content.content 

	except:
		print(requests.get(url, headers=user_agent, proxies=proxy).status_code)
		print(f'url {url} is not valid ')
		pass
#need one proxy
def get_category_list(url, proxy):
	content = get_content(url, proxy)
	content = bs(content, 'lxml')
	list_ = content.find('ul', class_='tabs')
	categories = []
	for i in list_:
		try:
			categories.append(i.find('a')['href'])
		except:
			pass
	categories_ = list_.find_all('li', class_='tab-collapsed')
	for i in categories_:
		categories.append(i.contents[0]['href'])
	
	return categories

# Возвращает все ссылки на вариации товара (отдельно труба 3.5мм, 4.0мм и тд)
def get_more_categories(url, proxies):
	content = get_content(url, proxies)
	content = bs(content, 'lxml')
	panel = content.find('div', class_='panes')
	print(panel)
	categories = []
	# a lot of <a></a> tags
	as_ = panel.find_all('a')
	for i in as_:
		print(i['href'])
		categories.append('https://23met.ru/',i['href'])
	return categories

def write_urls(categories):
	with open('urls.txt', 'a') as file:
		for i in categories:
			file.write(str(i) + "\n")   


if __name__ == '__main__':
	urls = ['/price/polosa_ocink/6х40',
	'/price/polosa_ocink/6х50',
	'/price/polosa_ocink/6х60',
	'/price/polosa_ocink/6х70',
	'/price/polosa_ocink/6х100',
	'/price/polosa_ocink/8х40',
	'/price/polosa_ocink/8х100',
	]
	logging.basicConfig(level=logging.INFO, filename='log.log')
	now = datetime.now()
	logging.info(f'program started at {now}')

	proxies = open('proxies.txt', 'r').read().split('\n')
	
	categories = get_category_list('http://23met.ru/price/', choice(proxies))
	all_categories = []
	for url in categories:
		all_categories.append(get_more_categories(url, proxies))
	print(len(all_categories))
	write_urls(all_categories)	
	logging.info(f'programs time is {datetime.now() - now}')
	print(datetime.now() - now)