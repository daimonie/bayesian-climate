import numpy as np
import pandas as pd
import os
import netCDF4
import logging
import time
logger = logging.getLogger()
logger.setLevel("INFO")

# about the dataset:
# http://berkeleyearth.org/data/ 
def toc(tic):
	toc = time.time()

	time_diff = toc - tic

	logging.info(f"Time passed is {time_diff} seconds.")

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
# File starts here
path='/opt/container/data/data.txt' 
path_out='/opt/container/data/data_processed.csv' 


start_time = time.time() 
toc(start_time)

df_raw = (
	read_data(path)
	.pipe(select_columns, [1, 2, 3], ["year", "month", "anomaly"])
)

print(df_raw.head(10))

toc(start_time)

logging.info("Writing to file")
df_raw.to_csv(path_out, index=False,)
toc(start_time)