import requests
from bs4 import BeautifulSoup as bs 
from datetime import datetime 
from pprint import pprint

from random import choice

import logging

from fake_useragent import UserAgent

import time

import csv

import sys

def get_content(url, proxy=None):
	#ua = UserAgent()
	#user_agent ={'User-Agent': ua.random}
	#proxy = {'http': 'http://'+ choice(proxy)}
	try:
		content = requests.get(url)
		#content = requests.get(url, headers=user_agent, proxies=proxy)
		return content.content 

	except:
		#print(requests.get(url, headers=user_agent, proxies=proxy).status_code)
		print(f'url {url} is not valid ')
		pass
#need one proxy
def get_category_list(url):
	content = get_content(url)
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
def get_more_categories(url):

	content = get_content(url)
	content = bs(content, 'lxml')
	panel = content.find('div', class_='panes')
	print(panel)
	categories = []
	# a lot of <a></a> tags
	as_ = panel.find_all('a')
	for i in as_:
		print(i['href'])
		categories.append(i['href'])
	return categories

def write_urls(categories):
	with open('urls.txt', 'a') as file:
		for i in categories:
			file.write(str(i) + "\n")   


def write_csv(product):
	print('starting writing in csv...')
	with open('file/products.csv', 'a', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=';')
		writer.writerow(product)
	print('ok')

def get_product_info(url):
	if url.find('http') == None:
		url = f"https://23met.ru/{url}"
	
	content = get_content(url)
	content = bs(content, 'lxml')
	table = content.find('table', class_='tablesorter')
	table_names = table.find_all('th')
	params = []
	for table_name in table_names:
			
			if table_name.text == 'Наименование':
				params.append('name')
			elif table_name.text == 'Марка стали':
				params.append('steel_mark')
			elif table_name.text == 'Размер':
				params.append('size')
			elif table_name.text == 'Длина':
				params.append('long')
			elif table_name.text == 'Толщина панели':
				params.append('panel_thickness')
			elif table_name.text == 'Толщина металла':
				params.append('metal_thickness')
			elif table_name.text == 'Рабочая ширина':
				params.append('working_height')
			elif table_name.text == 'Диаметр':
				params.append('diametr')
			elif table_name.text.find('Цена') != -1 and table_name.text.find("Цена1") == -1:
				params.append('cost')
			elif table_name.text.find('Цена1') != -1:
				params.append("cost1")
			elif table_name.text.find('Цена2') != -1:
				params.append('cost2')
			else:
				logging.info(f'table_name parameter {table_name.text} is not in all_categories')
				sys.exit(1)
	tbody = content.find('tbody')

	rows = tbody.find_all('tr')
	print(rows)
	all_categories = ['name','steel_mark','mark','size','long','panel_thickness','metal_thickness','diametr','cost','cost1','cost2,']
	# params = ['name', 'steel_mark', 'mark', 'cost']
	for row in rows:
		#print(row)
		product = []
		j = 0
		#Проверяем наличие параметра из all_categories в params товара. 
		#Если есть - вставляем, если нет - вставляем None
		for i in range(len(all_categories)):
			if all_categories[i] in params:
				print(row.find_all('td'))
				product.append(row.find_all('td')[j].text)
				j += 1
			else:
				product.append("None")
		write_csv(product)
		

#	params = []
#	for th in table.find_all('th'):
#		params.append(th.text)
#	print(params)

"""
конская залупа бесполезная
	name = False
	long_ = False
	metal_thickness = False
	panel_thickness = False
	diametr = False
	mark = False
	cost = False
	cost1 = False
	cost2 = False
	provider = False
	size = False
	working_height = False
	steel_mark = False
	params = []
	table_names = table.find_all('th')
	print(table_names)
"""
	
	#Получение всех столбцов товаров
		

"""
Дристня ненужная 
		if table_name.text == "Наименование":
			params.append('name')
		else:
			params.append(None)
		if table_name.text == "Марка стали":
			params.append('steel_mark')
		else:
			params.append(None)
		if table_name.text == 'Марка':
			params.append('mark')
		else:
			params.append(None)
		if table_name.text == 'Размер':
			params.append('size')
		else:
			params.append(None)
		if table_name.text == "Длина":
			params.append('long')
		else:
			params.append(None)
		if table_name.text == "Толщина панели":
			params.append('panel_thickness')
		else:
			params.append(None)
		if table_name.text == "Толщина металла":
			params.append('metal_thickness')
		else:
			params.append(None)
		if table_name.text == "Рабочая ширина":
			params.append('working_height')
		else:
			params.append(None)
		
		if table_name.text == 'Диаметр':
			params.append('diametr')
		else:
			params.append(None)
		if table_name.text.find("Цена") != None:
			params.append('cost')
		else:
			params.append(None)

		if table_name.text.find('Цена1') != None:
			params.append('cost1')
		else:
			params.append(None)

		if table_name.text.find("Цена2") != None:
			params.append('cost2')
		else:
			params.append(None)
	if(cost1 == True):
		cost = False
	print(params)
"""


if __name__ == '__main__':
	"""
	urls = ['/price/polosa_ocink/6х40',
	'/price/polosa_ocink/6х50',
	'/price/polosa_ocink/6х60',
	'/price/polosa_ocink/6х70',
	'/price/polosa_ocink/6х100',
	'/price/polosa_ocink/8х40',
	'/price/polosa_ocink/8х100',
	]
	"""
	logging.basicConfig(level=logging.INFO, filename='log.log')
	now = datetime.now()
	logging.info(f'program started at {now}')

	proxies = open('proxies.txt', 'r').read().split('\n')
	
	categories = get_category_list('http://23met.ru/price/')
	all_categories = []
	count = 0
	for url in categories:
		all_categories.append(get_more_categories(url))
		count +=1 
		if count % 5 == 0:
			time.sleep(30)
	print(len(all_categories))
	write_urls(all_categories)	
	logging.info(f'programs time is {datetime.now() - now}')
	print(datetime.now() - now)
	get_product_info('http://23met.ru/price/sandvich_paneli/стеновые')