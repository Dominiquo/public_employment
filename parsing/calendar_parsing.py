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
		self.min_date = None
		self.max_date = None
		self.is_valid = False

		self._transform_calendar()
		self._valid_calendar()

		# CONSTANTS
		self.no_date = datetime.fromtimestamp(0)
		self.difusion = 'Difu'
		self.final = 'Final'

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

	def _valid_calendar(self):
		min_date_field, min_date, _ = self.get_min_date()
		max_date_field, _ , max_date = self.get_max_date()
		valid_start = min_date_field.startswith(self.difusion)
		valid_end = max_date_field.startswith(self.final)
		not_epoch = (epoch_date != self.no_date) or (epoch_date != self.no_date)
		self.is_valid = (valid_start and valid_end and (not self.inverted_dates) and not_epoch)
		return self.is_valid

	def days_open(self):
		if self.is_valid:
			try:
				_, open_d, close_d = self.max_date
				# returns a timedelta object so .days is a method of TimeDelta
				return (close_d - open_d).days
			except Exception as e:
				return -1
		return None

	def days_selection(self):
		if self.is_valid:
			try:
				_, open_d_start, close_d_start = self.max_date
				_, open_d_final, close_d_final = self.min_date
				# returns a timedelta object so .days is a method of TimeDelta
				return (close_d_start - close_d_start).days
			except Exception as e:
				return -1
		return None

	def process_time(self):
		if self.is_valid:
			try:
				_, open_d_start, close_d_start = self.max_date
				_, open_d_final, close_d_final = self.min_date
				# returns a timedelta object so .days is a method of TimeDelta
				return (close_d_final - open_d_start).days
		return None

	def get_min_date(self):
		self.min_date = ('', self.no_date, self.no_date)
		if self.cal_parsed != []:
			 self.min_date = min(self.cal_parsed, key=lambda v: v[1])
		return self.min_date

	def get_max_date(self):
		self.max_date = ('', self.no_date, self.no_date)
		if self.cal_parsed != []:
			self.max_date = max(self.cal_parsed, key=lambda v: v[2])
		return self.max_date



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