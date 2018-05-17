import os
import numpy as np
import pandas as pd
import pickle
from parsing import PostingHandler
from utils import constants



def load_all_pages(page_dir, limit=float('inf')):
	all_pages_text = []
	print('loading pages...')
	for ix,page_file in enumerate(os.listdir(page_dir)):
		if ix > limit:
			# put an upper limit to reduce runtime during sampling
			break
		if page_file.endswith('.html'):
			full_path = os.path.join(page_dir, page_file)
			with open(full_path, encoding="ISO-8859-1") as infile:
				page_id = get_page_id(page_file)
				all_pages_text.append((page_id, infile.read()))
	return all_pages_text


def get_page_id(filename):
	underscore = '_'
	if underscore in filename:
		num = filename.split(underscore)[0]
	try:
		return int(num)
	except Exception as e:
		print('Page ID not found')
		return -1
	return -1


def page_to_fields(page_text, page_id):
	page_obj = PostingHandler.PostingParser(page_text, page_id)
	return page_obj.get_parse_dict()


def get_all_page_fields(page_dir, limit=float('inf')):
	all_pages = load_all_pages(page_dir, limit)
	print('extracting information from pages...')
	return [page_to_fields(page_text, p_id) for p_id, page_text in all_pages]


def get_all_page_main_fields(all_page_fields):
	print('compiling list of all possible main field columns..')
	all_main_fields = []
	for pfields in all_page_fields:
		if pfields[constants.MAIN_FIELDS]:
			mfields = pfields[constants.MAIN_FIELDS]
			all_main_fields.append([pair[0] for pair in mfields])
	flattened = [item for sublist in all_main_fields for item in sublist]
	return set(flattened)


def make_df_all_pages(page_dir, limit=float('inf')):
	all_page_fields = get_all_page_fields(page_dir, limit)
	columns_set = get_all_page_main_fields(all_page_fields)
	df_dict = {key:[] for key in columns_set}
	for page_fields in all_page_fields:
		main_fields = page_fields[constants.MAIN_FIELDS]
		cal_fields = page_fields[constants.CALENDAR]
		# check that value isn't None
		if main_fields:
			added_main = set([v[0] for v in main_fields])
			assert len(added_main) == len(main_fields)
			for key,val in main_fields:
				df_dict[key].append(val)
			level_df_dict(df_dict, columns_set, added_main)
		if cal_fields:
			for field_name, days_count in cal_fields.items():
				if field_name in df_dict:
					df_dict[field_name].append(days_count)
				else:
					df_dict[field_name] = [days_count]
	return pd.DataFrame(df_dict)


def level_df_dict(df_dict, columns_set, added_main):
	# Fill in rows with None vals that were missing in the pages main fields
	add_vals = columns_set - added_main
	for col in add_vals:
		df_dict[col].append(np.nan)
	return df_dict


def add_results_df(dataframe, results_file, id_col=constants.ID_FIELD):
	results = 'RESULTS'
	try:
		results_df = pd.read_csv(results_file, index_col=0)
		results_dict = results_df.to_dict(orient='index')
		add_result = lambda id_val: results_dict[id_val][results] if id_val in results_dict else np.nan
		dataframe[results] = dataframe[id_col].apply(add_result)
		return dataframe
	except Exception as e:
		print('Cannot add results.')
		return dataframe


def add_results_category(dataframe):
	val_categories = set([constants.DESIERTO,
							constants.SIN_RESULTADO,
							constants.SIN_EFECTO])
	HAS_RESULT = 'RESULT'
	dataframe[constants.RESULT_CAT] = dataframe[constants.RESULTS].apply(
										lambda v: v if v in val_categories else HAS_RESULT)
	return dataframe


def get_ministry_sizes(ministry_path='data/ministry_budget.csv'):
	ministry = 'MINISTRY'
	personnel_budget = 'personnel_budget'
	bad_ministry_val = 'Ministerio de PlanificaciÃ³n'
	df_min = pd.read_csv(ministry_path)

	ministry_value_dict = {}
	ministry_value_dict['Autónomo'] = np.nan
	for i,row in df_min.iterrows():
		ministry_value_dict[row[ministry]] = row[personnel_budget]

	return ministry_value_dict