import os
import pandas as pd
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
			with open(full_path) as infile:
				all_pages_text.append(infile.read())
	return all_pages_text


def page_to_fields(page_text):
	page_obj = PostingHandler.PostingParser(page_text)
	return page_obj.get_parse_dict()


def get_all_page_fields(page_dir, limit=float('inf')):
	all_pages = load_all_pages(page_dir, limit)
	print('extracting information from pages...')
	return [page_to_fields(page_text) for page_text in all_pages]


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
		# check that value isn't None
		if main_fields:
			added_main = set([v[0] for v in main_fields])
			assert len(added_main) == len(main_fields)
			for key,val in main_fields:
				df_dict[key].append(val)
			level_df_dict(df_dict, columns_set, added_main)
	return pd.DataFrame(df_dict)


def level_df_dict(df_dict, columns_set, added_main):
	# Fill in rows with None vals that were missing in the pages main fields
	add_vals = columns_set - added_main
	for col in add_vals:
		df_dict[col].append(None)
	return df_dict


