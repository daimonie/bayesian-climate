import pandas as pd
import numpy as np


def read_data(path):
	df_raw = pd.read_fwf(
		path,
		skiprows=86
	)
	initial_columns = df_raw.columns.values
	first_row = df_raw.head(1).values.T

	final_columns = {}
	for i in range(len(initial_columns)):
		initial = initial_columns[i]
		row=first_row[i, 0]
		final_columns[initial] = f"{initial} {row}"

	df_raw = (
		df_raw
		.rename(columns=final_columns)
		.drop(0) #the first row contained some column names, now they're dropped
	)
	return df_raw
 
def select_columns(df, column_indices, column_names):
	"""Returns a dataframe with the selected columns"""
	df_data = df.copy()
	columns = df_data.columns.values[column_indices]

	final_columns = {}
	for i in range(len(columns)):
		old_name = columns[i]
		new_name = column_names[i]
		final_columns[old_name] = new_name

	df_final = df_data[columns].rename(columns=final_columns)
	
	return df_final

def safe_int(x):
    try:
        return int(x)
    except:
        return np.nan

def safe_float_from_object(obj, index=0, seperator=" "):
    try:
        data = obj.split(seperator)
        x = data[index]
        return float(x)
    except:
        return np.nan
def set_dtypes(df):
    df_data = (
        df
        .copy()
    )
    df_final = (
        df_data
        .assign(
            year = df_data.year.apply(safe_int),
            month = df_data.month.apply(safe_int),
            anomaly = [safe_float_from_object(_, index=0, seperator="  ") for _ in df_data.anomaly.values],
            anomaly_std = [safe_float_from_object(_, index=1, seperator="  ") for _ in df_data.anomaly.values]
        )
    )
    return df_final