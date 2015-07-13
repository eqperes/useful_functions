'''
Used to obtain averages of some elements in a Pandas DataFrame and then setting other elements with the averages obtained
'''

import pandas as pd

def category_averaging(df, filter_column, filter_value, category_column, value_columns):

	df_filtered = df[df[filter_column] == filter_value]
	averages = df_filtered.groupby(category_column).mean()
	averages = averages.loc[:, value_columns]

	df_to_set = df[df[filter_column] != filter_value]
	df.loc[df_to_set.index, value_columns] = averages.loc[df_to_set[category_column]].values
	
