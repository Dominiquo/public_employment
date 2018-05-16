import pandas as pd
from bs4 import BeautifulSoup
import os
import json
import re
from utils import constants
from parsing import calendar_parsing as cp

class PostingParser(object):
	'''extract different parts from an html page of a public sector job posting
		Initialize: 
			input: html_text; string of html structured text from job postings

	'''

	def __init__(self, html_text, page_id):
		self.page_obj = BeautifulSoup(html_text, 'html.parser')
		self.page_id = page_id
		self.main_fields = None
		self.time_table = None
		self.cal_obj = None
		self.cal_values = None
		# constants
		self.MAIN_FIELDS_ID = 'lblAvisoTrabajoDatos'
		self.ID_FIELD = 'PAGE_ID'

	def get_parse_dict(self):
		result_dict = {}
		result_dict[constants.ID_FIELD] = self.page_id
		result_dict[constants.MAIN_FIELDS] = self.parse_main_fields()
		result_dict[constants.CALENDAR] = self.get_cal_info()
		return result_dict

	def parse_main_fields(self):
		kv_pairs = [(self.ID_FIELD, self.page_id)]
		section = self.page_obj.find(id=self.MAIN_FIELDS_ID)
		if not section:
			return kv_pairs
		list_section = section.find_all(constants.LIST_ITEM)
		for list_item in list_section:
			# eliminate duplicates
			if list_item.find(constants.UNORDERED_BULLET) == None:
				key_tag = list_item.find(constants.BOLD_TAG)
				if key_tag != None:
					key = key_tag.text
					# remove text that isn't bold because there is not tag for value
					value = list_item.text[len(key):]
					kv_pairs.append((key, value))
		self.main_fields = kv_pairs
		return kv_pairs

	def get_cal_obj(self):
		if self.time_table == None:
			self.extract_table()
		self.cal_obj = cp.CalendarParser(self.time_table, self.page_id)
		return self.cal_obj

	def get_cal_info(self):
		if self.cal_obj == None:
			self.get_cal_obj()
		cal_vals = {constants.DAYS_OPEN: None,
					constants.DAYS_SELECT: None,
					constants.PROC_TIME: None,
					constants.YEAR: None,
					constants.MONTH: None}
		if self.cal_obj.get_is_valid():
			cal_vals[constants.DAYS_OPEN] = self.cal_obj.get_days_open()
			cal_vals[constants.DAYS_SELECT] = self.cal_obj.get_days_selection()
			cal_vals[constants.PROC_TIME] = self.cal_obj.get_process_time()
			cal_vals[constants.YEAR] = self.cal_obj.get_year()
			cal_vals[constants.MONTH] = self.cal_obj.get_month()

		self.cal_values = cal_vals
		return self.cal_values

	def extract_table(self):
		tables = self.page_obj.find_all(constants.TABLE)
		time_table = None	
		for table in tables:
			if constants.FASE in table.text:
				time_table = table
		self.time_table = time_table
		return time_table

