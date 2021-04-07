import numpy as np
import pandas as pd
import os
import netCDF4
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def process_nc_data(path):
	nc = netCDF4.Dataset(path)
	nc_dim_time = nc.dimensions['time'] 

	nc_var_time = nc.variables['time']
	nc_var_temperature = nc.variables['temperature']

	xlabel = nc_dim_time.name
	ylabel = nc_var_temperature.long_name
	
	shape = nc_var_temperature.shape

	data_array = []

	xmax = shape[0]
	ymax = shape[1]
	#ymax = 100
	for i in range(0, xmax):
		x = nc_var_time[i]
		progress = int(i/shape[0]*1000)/10
		logging.info(f"Processing data for t={x}, {progress}%")
		for j in range(0, ymax):
			y = nc_var_temperature[i,j]
			data_array.append([x,y])

	
	return pd.DataFrame(
		data=data_array,
		columns=[xlabel, ylabel]
	)
path='/opt/container/data/dataset.nc'
path_out='/opt/container/data/data_processed.csv'

if os.path.exists(path_out)  is False:
	df_data = process_nc_data(path)
	logging.info(df_data.head())
	df_data.to_csv(path_out, index=False, compression='gzip')
	logging.info("Data has been processed.")
	logging.info(f"See {path_out}")
else:
	logging.info("Data has been processed previously.")
	logging.info(f"See {path_out}")