import matplotlib as plt
from parsing import PostingHandler, aggregate
from analysis import transformation_pipeline
from utils import constants
from datetime import datetime
import pandas as pd
import numpy as np


def job_dist_by_date_plot(dataframe):
	title = 'Job Postings by Date'
	dataframe = get_time_month_df(dataframe)
	dataframe[constants.TIME_OBJ].value_counts().plot(title=title)
	return None


def posting_dist_by_month_plot(dataframe):
	title = 'Distribution by Month'
	dataframe[constants.MONTH].value_counts().sort_index().plot(kind='bar', title=title)
	return None

def ministry_size_normalize_plot(dataframe):
	title = 'Postings By Department Normalized by Budget'
	vcount = ministry_size_normalized_df(dataframe)
	vcount[constants.SIZE].sort_values(ascending=False).plot(kind='bar', title=title)
	return None

def ministry_by_size_plot(dataframe):
	title = 'Ministry Size by Number of Postings'
	df = transformation_pipeline.update_ministry_name(dataframe)
	vcount = df[constants.MINISTRY].value_counts().to_frame()
	vcount[constants.MINISTRY].sort_values(ascending=False).plot(kind='bar', title=title)
	return None

def ministry_num_vac_normalize_plot(dataframe):
	title = 'Ministry by Total Number of Vacanies'
	job_dist = ministry_num_vac_normalize_df(dataframe)
	job_dist[constants.SUM_COL].sort_values(ascending=False).plot(kind='bar', title=title)
	return None

def ministry_num_vac_budget_plot(dataframe):
	title = 'Ministry Size by Postings Normalized by Budget'
	job_dist = ministry_num_vac_normalize_df(dataframe)
	sizes = get_size_dict()
	rowIndex = lambda row: row.name
	job_dist[constants.SUM_COL] = job_dist.apply(lambda row: row[constants.SUM_COL]/sizes[rowIndex(row)], axis=1)
	job_dist = job_dist[job_dist[constants.SUM_COL].notnull()]
	job_dist[constants.SUM_COL].sort_values(ascending=False).plot(kind='bar', title=title)
	return None

def wage_by_month_plot(dataframe):
	title = 'Average Gross Salary Offered By Month of Year'
	df_grouped = dataframe.groupby(constants.MONTH).agg({constants.WAGE_V: [np.mean]})
	df_grouped.columns = df_grouped.columns.droplevel(0)
	df_grouped.plot(title=title)
	return None

def wage_by_month_all_plot(dataframe):
	title = 'Average Gross Salary Offered By Month All'
	dataframe = get_time_month_df(dataframe)
	df_grouped = dataframe.groupby(constants.TIME_OBJ).agg({constants.WAGE_V: [np.mean]})
	df_grouped.columns = df_grouped.columns.droplevel(0)
	df_grouped.plot(title=title)
	return None

def wage_by_ministry_plot(dataframe, threshold=75):
	count_col = 'count'
	mean_col = 'mean'
	dataframe = transformation_pipeline.update_ministry_name(dataframe)
	sub_df = dataframe.groupby(constants.MINISTRY).agg({constants.WAGE_V:[np.mean, count]})
	sub_df.columns = sub_df.columns.droplevel(0)
	sub_df = sub_df[sub_df[count_col] > threshold]
	sub_df[mean_col].sort_values(ascending=False).plot(kind='bar')
	return None

def vac_type_dist(dataframe):
	title = 'Vacancy Type Distribution'
	dataframe[constants.VAC_TYP].value_counts().plot(kind='bar', title=title)
	return None

def wage_by_vac_type_plot(dataframe):
	mean_col = 'mean'
	title = 'Average Wage by Vacancy Type'
	sub_df = dataframe.groupby(constants.VAC_TYP).agg({constants.WAGE_V:[np.mean, count]})
	sub_df.columns = sub_df.columns.droplevel(0)
	sub_df[mean_col].plot(kind='bar', title=title)
	return None

def schedule_by_month_plot(dataframe):
	title = 'Time Schedule by Month'
	dataframe.groupby(constants.MONTH).agg({constants.DAYS_OPEN: [np.mean],
                        constants.DAYS_SELECT: [np.mean],
                        constants.PROC_TIME: [np.mean]}).plot(title=title)
	return None

def days_open_ministry_plot(dataframe, threshold=75):
	title = 'Days Open by Ministry'
	mean_col = 'mean'
	ministry_by_days_df = days_open_ministry_df(dataframe, threshold=threshold)
	ministry_by_days_df[mean_col].sort_values(ascending=False).plot(kind='bar', title=title)
	return None

def days_open_by_month_all_plot(dataframe):
	title = 'Average Days Open by Date'
	dataframe = get_time_month_df(dataframe)
	df_grouped = dataframe.groupby(constants.TIME_OBJ).agg({constants.DAYS_OPEN: [np.mean]})
	df_grouped.columns = df_grouped.columns.droplevel(0)
	df_grouped.plot(title=title)
	return None

def days_open_contract_type_plot(dataframe):
	title = 'Days Open By Vacancy Type'
	dataframe.groupby(constants.VAC_TYP).agg({constants.DAYS_OPEN: np.mean}).plot(kind='bar', title=title)
	return None

def results_by_contract_type_plot(dataframe):
	title = 'Result Distribution by Vacancy Type'
	dist_df = results_dist_df(dataframe, constants.VAC_TYP)
	dist_df.plot(kind='bar', title=title)
	return None

def results_by_ministry_plot(dataframe, threshold=75):
	title = 'Results Distribution by Ministry'
	dataframe = transformation_pipeline.update_ministry_name(dataframe)
	dataframe = threshold_filter(dataframe, constants.MINISTRY, threshold)
	dist_df = results_dist_df(dataframe, constants.MINISTRY)
	dist_df.plot(kind='bar', title=title)
	return None

def results_by_month_plot(dataframe, threshold=100):
	result_col = 'RESULT'
	title = 'Percentage of Posting with Results by Month'
	dataframe = threshold_filter(dataframe, constants.MONTH, threshold)
	dataframe = results_dist_df(dataframe, constants.MONTH)
	dataframe[result_col].plot(title=title)
	return None

def results_by_date_plot(dataframe, threshold=100):
	result_col = 'RESULT'
	title = 'Percentage of Postings with Results by Date'
	dataframe = get_time_month_df(dataframe)
	dataframe = threshold_filter(dataframe, constants.TIME_OBJ, threshold)
	dataframe = results_dist_df(dataframe, constants.TIME_OBJ)
	dataframe[result_col].plot(title=title)
	return None




########################## DATAFRAME BUILDER ###############################
def get_time_month_df(dataframe):
	dataframe[constants.TIME_OBJ] = dataframe[[constants.MONTH, constants.YEAR]].apply(
							lambda r: year_month(r[constants.YEAR], r[constants.MONTH]), axis=1)
	return dataframe[dataframe[constants.TIME_OBJ].notnull()]


def ministry_num_vac_normalize_df(dataframe):
	title = 'Ministry by Total Vacanies'
	dataframe = transformation_pipeline.update_ministry_name(dataframe)
	dataframe[constants.VACANCIES] = dataframe[constants.VACANCIES].apply(to_int)
	job_dist = dataframe.groupby(constants.MINISTRY).agg({constants.VACANCIES: [sum, np.mean, len]})
	job_dist.columns = job_dist.columns.droplevel(0)
	return job_dist


def ministry_size_normalized_df(dataframe):
	df = transformation_pipeline.update_ministry_name(dataframe)
	sizes = get_size_dict()
	vcount = df[constants.MINISTRY].value_counts().to_frame()
	rowIndex = lambda row: row.name
	vcount[constants.SIZE] = vcount.apply(lambda row: row[constants.MINISTRY]/sizes[rowIndex(row)], axis=1)
	return vcount[vcount[constants.SIZE].notnull()]

def days_open_ministry_df(dataframe, threshold=75):
	count = 'count'
	dataframe = transformation_pipeline.update_ministry_name(dataframe)
	grouped_df =  dataframe.groupby(constants.MINISTRY).agg(
						{constants.DAYS_OPEN: [np.mean, np.std, count]})
	grouped_df.columns = grouped_df.columns.droplevel(0)
	grouped_df = grouped_df[grouped_df[count] > threshold]
	return grouped_df

def results_dist_df(dataframe, comp_col):
	result_cat_count = dataframe.groupby([comp_col, constants.RESULT_CAT]).agg({constants.RESULTS: count})
	dist_df = result_cat_count.groupby(level=0).apply(lambda x: 100*x/float(x.sum()))
	dist_df = dist_df.unstack()
	dist_df.columns = dist_df.columns.droplevel(0)
	return dist_df

def threshold_filter(dataframe, column, threshold=100):
	counts_series = dataframe[column].value_counts()
	counts_series = counts_series[counts_series > threshold]
	return dataframe[dataframe[column].isin(counts_series.index)]

########################## HELPER ###############################

def to_int(v):
    try:
        return int(v)
    except:
        return np.nan


def year_month(year, month):
    if pd.notnull(year) and pd.notnull(month):
        return datetime(year=int(year), month=int(month), day=1)
    return np.nan


def get_size_dict():
	sizes = aggregate.get_ministry_sizes(ministry_path='data/ministry_budget.csv')
	sizes[''] = np.nan
	sizes[' '] = np.nan
	sizes['TESORO PÚBLICO'] = np.nan
	return sizes


def count(x):
     return x.count()

