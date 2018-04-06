import urllib.request
from bs4 import BeautifulSoup
from utils import constants
import os


def produce_link(app_type, index):
	full_link = (constants.POSTING_BASE_LINK + 
				app_type + 
				constants.INTERMEDIATE + 
				str(index))
	return full_link


def fetch_html(full_url):
	try:
		with urllib.request.urlopen(full_url) as response:
			page = response.read()
	except Exception as e:
		print(e)
		page = constants.EMPTY_PAGE
	return page


def store_file(html_page, tipo, index, store_dir=constants.STORE_POSTINGS):
	name = str(index) + '_' + tipo
	extension = '.html'
	filename =  name + extension
	full_path = os.path.join(store_dir, full_path)
	try:
		with open(full_path, 'w') as outfile:
			outfile.write(html_page)
		return True
	except Exception as e:
		print(e)
	return False


def main():
	tipo = constants.TYPE_LIST[2]  # 'avisopizarronficha'
	for index in range(1, 32942):
		link = produce_link(tipo, index)
		print('fetching application index', index)
		html_page = fetch_html(link)
		store_file(html_page, tipo, index)
	return True
