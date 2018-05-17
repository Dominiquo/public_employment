from utils import tools
import numpy as np
import pandas as pd
from parsing import PostingHandler, aggregate
from utils import constants

def create_clean_df(pages_fp, results_fp, limit=float('inf')):
	df = aggregate.make_df_all_pages(pages_fp, limit)
	df = clean_ministerio(df)
	df = aggregate.add_results_df(df, results_fp)
	df = aggregate.add_results_category(df)
	df = clean_wage_col(df)
	return df

def clean_wage_col(dataframe):
	print('cleaning wage string..')
	dataframe[constants.WAGE_V] = dataframe[constants.WAGE_OG].apply(clean_wage_str)
	return dataframe

def update_ministry_name(dataframe):
	dataframe = clean_ministerio(dataframe)
	dataframe[constants.MINISTRY] = dataframe[constants.MINISTRY].apply(lambda v: constants.MINISTRY_MAP[v])
	return dataframe

def clean_ministerio(dataframe):
	print('removing nan ministerio values...')
	dataframe = dataframe[dataframe[constants.MINISTRY].notnull()]
	dataframe = dataframe[dataframe[constants.MINISTRY] != '']
	return dataframe

def clean_wage_str(wage_str):
	try:
		if pd.notnull(wage_str):
			return int(wage_str.replace('.',''))
	except Exception as e:
		pass
	return np.nan