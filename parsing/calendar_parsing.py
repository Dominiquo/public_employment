from parsing import PostingHandler
import pandas as pd
from bs4 import BeautifulSoup
import os
import json
import re
from utils import constants
from datetime import datetime


class CalendarParser(object):
	def __init__(self, cal_table, page_id):
		self.calendar_list = cal_table
		self.page_id = page_id
		self.cal_parsed = None
		self.inverted_dates = False
		self._transform_calendar()

	def _transform_calendar(self):
		if self.cal_parsed:
			return self.cal_parsed
		else:
			self.cal_parsed = []
		for cell_name, date_string in self.calendar_list:
			first, last = datetime_translate(date_string)
			if not first <= last:
				self.inverted_dates = True
			self.cal_parsed.append((cell_name, first, last))
		return self.cal_parsed

	def days_open(self):
		return None

	def days_selection(self):
		return None

	def process_time(self):
		return None

	def get_min_date(self):
		if self.cal_parsed != []:
			return min(self.cal_parsed, key=lambda v: v[1])
		return ('', -1, -1)

	def get_max_date(self):
		if self.cal_parsed != []:
			return max(self.cal_parsed, key=lambda v: v[2])
		return ('', -1, -1)



def datetime_translate(dt_string):
		# Split string
		STRING_FORMAT = '%d/%m/%Y'
		try:
			start, end = dt_string.split('-')
			start_obj = datetime.strptime(start, STRING_FORMAT)
			end_obj = datetime.strptime(end, STRING_FORMAT)
		except Exception as e:
			print(e)
			return datetime.fromtimestamp(0), datetime.fromtimestamp(0)

		return start_obj, end_obj