import pandas as pd
from bs4 import BeautifulSoup
import os
import json
import re
from utils import constants

def html_to_bso(html_page_text):
	return BeautifulSoup(html_page, 'html.parser')


def extract_date(json_data):
	dates_data = json_data[constants.CALENDAR]
	dates_obj = None
	try:
		date_str = dates_data[0][1][:10]
		dates_obj = datetime.strptime(date_str, constants.DT_FORMAT)
	except Exception as e:
		pass
	return dates_obj


def extract_table(html_page):
	bs_obj = html_to_bso(html_page)
	tables = bs_obj.find_all(constants.TABLE)
	time_table = None
	for table in tables:
	    if constants.FASE in table.text:
	        time_table = table
	return time_table


def parse_calendar(page_bs_obj):
	tables = page_bs_obj.find_all(constants.TABLE)
	time_table = None	
	for table in tables:
		if constants.FASE in table.text:
			time_table = table

	if time_table == None:
		return []
	else:
		all_rows = time_table.find_all(constants.ROW)

	table_vals = []
	for row_obj in all_rows:
		all_cells = row_obj.find_all(constants.CELL)
		if len(all_cells) > 1 and all_cells[0].text != constants.FASE:
			table_vals.append((all_cells[0].text, all_cells[1].text))

	return table_vals


def parse_main_fields(page_bs_obj):
	section_id = 'lblAvisoTrabajoDatos'
	list_item_tag = 'li'
	bold_tag = 'b'
	section = page_bs_obj.find(id=section_id)
	list_section = section.find_all(list_item_tag)
	kv_pairs = []
	for list_item in list_section:
		key_tag = list_item.find(bold_tag)
		if key_tag != None:
			key = key_tag.text
			value = list_item.text[len(key):]
			kv_pairs.append((key, value))
	return kv_pairs



def check_column(directory):
	ignore_file = '.DS_Store'
	all_data = {}
	all_files = os.listdir(directory)
	n_files = len(all_files)
	prev_cols = []
	truth = []
	for i,filename in enumerate(all_files):
		if filename == ignore_file: continue
		print('parsing file:', filename, i, '/', n_files)
		filepath = os.path.join(directory, filename)
		page_obj = get_bs_obj(filepath)
		main_fields = parse_main_fields(page_obj)
		calendar = parse_calendar(page_obj)
		current_cols = [v[0] for v in main_fields]
		for f,s in calendar:
			current_cols.append(f)
		is_same = (current_cols == prev_cols)
		truth.append((is_same, filename))
		print('is the same:', is_same)
		prev_cols = current_cols
	return truth

	



def extract_data(directory, storage_path):
	ignore_file = '.DS_Store'
	all_files = os.listdir(directory)
	n_files = len(all_files)
	current_files = load_read_files(storage_path)
	for i,filename in enumerate(all_files):
		if filename == ignore_file: continue
		if filename in current_files: continue
		print('parsing file:', filename, i, '/', n_files)
		filepath = os.path.join(directory, filename)
		try:
			page_obj = get_bs_obj(filepath)
			main_fields = parse_main_fields(page_obj)
			calendar = parse_calendar(page_obj)
			add_data(filename, storage_path, main_fields, calendar)
		except Exception as e:
			print('******************************')
			print(e)
			print(filename)
			pass
	return True


def load_read_files(storage_path):
	all_files = []
	with open(storage_path) as readfile:
		for line in readfile:
			j_val = json.loads(line)
			all_files.append(j_val['filename'])
	return set(all_files)


def add_data(filename, storage_path, main_fields, calendar):
	data = {'filename': filename,
			'main_fields': main_fields,
			'calendar': calendar}

	with open(storage_path, 'a') as outfile:
		json.dump(data, outfile)
		outfile.write('\n')
		
	return True


def get_bs_obj(filepath):
	with open(filepath) as infile:
		page_text = infile.read()

	return BeautifulSoup(page_text, 'html')


def sample_calendar_parse():
	fname = 'stored_pages/199_avisopizarronficha.html'
	with open(fname) as infile:
		page_text = infile.read()

	return BeautifulSoup(page_text, 'html')


# if __name__ == "__main__":
# 	extract_data('stored_pages','CALENDAR_FIELDS.txt')

