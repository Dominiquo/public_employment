import pandas as pd
from bs4 import BeautifulSoup
import os
import json
import re
from utils import constants

class PostingParser(object):
	'''extract different parts from an html page of a public sector job posting
		Initialize: 
			input: html_text; string of html structured text from job postings

	'''

	def __init__(self, html_text):
		self.page_obj = BeautifulSoup(html_text, 'html.parser')
		self.main_fields = None

		# constants
		self.MAIN_FIELDS_ID = 'lblAvisoTrabajoDatos'
		self.TABLE = 'table'
		self.FASE = 'Fase'

	def parse_main_fields(self):
		section = self.page_obj.find(id=self.MAIN_FIELDS_ID)
		list_section = section.find_all(constants.LIST_ITEM)
		kv_pairs = []
		for list_item in list_section:
			key_tag = list_item.find(constants.BOLD_TAG)
			if key_tag != None:
				key = key_tag.text
				# remove text that isn't bold because there is not tag for value
				value = list_item.text[len(key):]
				kv_pairs.append((key, value))
		self.main_fields = kv_pairs
		return kv_pairs

	def parse_calendar(self):
		time_table = self.extract_table()
		if time_table == None: return []
		all_rows = time_table.find_all(constants.ROW)
		table_vals = []
		for row_obj in all_rows:
			all_cells = row_obj.find_all(constants.CELL)
			if len(all_cells) > 1 and all_cells[0].text != self.FASE:
				table_vals.append((all_cells[0].text, all_cells[1].text))
		return table_vals

	def extract_table(self):
		tables = self.page_obj.find_all(self.TABLE)
		time_table = None	
		for table in tables:
			if self.FASE in table.text:
				time_table = table
		return table

