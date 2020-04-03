from db import *
import time
import datetime

from urllib.request import urlopen
from bs4 import BeautifulSoup



def parse(con, cur):
	print("Parsing Tesco")

	tesco_url = 'https://ezakupy.tesco.pl/groceries/pl-PL/'
	category_links = get_category_links(tesco_url)

	start_time = time.time()
	for link in category_links:
		products_url = tesco_url + link['href'].replace('?include-children=true', '/all')[1:]
		pages_number = number_of_pages(products_url)
		for page in range(1, pages_number):
			product_url = products_url+'?page='+str(page)
			products_html_page = urlopen(product_url).read()
			products_page_data = BeautifulSoup(products_html_page.decode('utf-8', 'ignore'), 'html.parser')
			products = products_page_data.findAll('li', attrs={'class': 'product-list--list-item'})
			for product in products:

				product_id = product.find('input', {'name':'id'})['value']
				product_name = product.find('a', {'data-auto':'product-tile--title'}).text
				img_url = product.find('img', {'class':'product-image'})['src']
				price = product.find('div', {'class':"price-control-wrapper"}).find('span', {'class':'value'}).text
				product_currency = product.find('div', {'class':"price-control-wrapper"}).find('span', {'class':'currency'}).text

				one_product_price = product.find('div', {'class':"price-per-quantity-weight"}).find('span', {'class':'value'}).text
				one_product_currency = product.find('div', {'class':"price-per-quantity-weight"}).find('span', {'class':'currency'}).text
				save_product(cur, 3, product_url, product_name, img_url, price)
				con.commit()

	finish_time = time.time() - start_time

	print("Tesco parsed in:", str(datetime.timedelta(seconds=finish_time)))


def number_of_pages(products_url):
	products_html_page = urlopen(products_url).read()
	products_page_data = BeautifulSoup(products_html_page, 'html.parser')
	pages = products_page_data.find('nav', {'class':"pagination--page-selector-wrapper"}).find_all('span', {'aria-hidden':'true'})
	pages_list = []
	for page in pages:
		if page.text != '':
			pages_list.append(int(page.text))

	return max(pages_list)


def get_category_links(tesco_url):
	page = urlopen(tesco_url).read()
	soup = BeautifulSoup(page, 'html.parser')
	category_links = soup.findAll('a', attrs={'class': 'menu__link--superdepartment'})
	return category_links
