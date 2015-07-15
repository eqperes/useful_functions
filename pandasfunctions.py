

import pandas as pd

def category_averaging(df, filter_column, filter_value, category_column, value_columns):
	'''
	Used to obtain averages of some elements in a Pandas DataFrame and then setting other elements with the averages obtained
	'''

	df_filtered = df[df[filter_column] == filter_value]
	averages = df_filtered.groupby(category_column).mean()
	averages = averages.loc[:, value_columns]

	df_to_set = df[df[filter_column] != filter_value]
	df.loc[df_to_set.index, value_columns] = averages.loc[df_to_set[category_column]].values
	
	
def expand_values(df, source_column, default_column, null_value="", new_column=True, new_column_name="New", split_char=";"):
	'''
	Used to generate multiple rows from a single row that contains concatenated values in one column
	'''
	
	if not new_column:
		new_column_name = source_column
	
	new_df = pd.DataFrame()
	for __, row in df.iterrows():
		if (row[source_column] == null_value):
            		new_row = row
            		new_row[new_column_name] = row[default_column]
            		new_df = new_df.append(new_row)
            	else:
            		values = row[source_column].split(split_char)
            		for value in values:
            			new_row = row
            			new_row[new_column_name] = value
            			new_df = new_df.append(new_row)
        
        return new_df
            	
	
