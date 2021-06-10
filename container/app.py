import numpy as np
import pandas as pd
import os
import netCDF4
import logging
import time
import seaborn as sns
import matplotlib.pyplot as plt

import bayesian_climate.climate as climate_lib
from bayesian_climate.utils import toc, plot_posterior
from bayesian_climate.wrangling import (
	read_data,
	select_columns,
	set_dtypes
)
logger = logging.getLogger()
logger.setLevel("INFO")

# about the dataset:
# http://berkeleyearth.org/data/ 
# File starts here
path='/opt/container/data/data.txt' 
path_out='/opt/container/data/data_processed.csv' 
path_simple_lmplot = '/opt/container/figures/00_simple_lmplot.png'
path_gamma_posterior = '/opt/container/figures/01_gamma_posterior.png'
path_err_posterior = '/opt/container/figures/02_err_posterior.png'

start_time = time.time() 
toc(start_time)
if os.path.exists(path_out) is False:

	logging.info(f"Reading file {path}.")
	df_raw = (
		read_data(path)
		.pipe(select_columns, [1, 2, 3], ["year", "month", "anomaly"])
	)

	logging.info(df_raw.head(10))

	toc(start_time)

	logging.info("Writing to file")
	df_raw.to_csv(path_out, index=False,)
	toc(start_time)
else:
	logging.info(f"Reading file {path_out}.")
	df_raw = pd.read_csv(path_out)
	logging.info(df_raw.head())
	logging.info(df_raw.dtypes)
	df_processed = (
	    df_raw
	    .pipe(set_dtypes)
	)
	logging.info(df_processed.dtypes)
	logging.info(df_processed.head())

	logging.info(f"Saving Figure to file {path_simple_lmplot}.")
	sns_plot = sns.lmplot(
		data=df_processed,
		x='year',
		y='anomaly',
		height=7,
		aspect=2
	)
	sns_plot.savefig(path_simple_lmplot)

	toc(start_time)
	model = climate_lib.fit_bayesian_quadratic(
		df_processed,
		sample_size=1500
	)
	toc(start_time)
 
	gamma_trace = model.get("gamma")
	plot_posterior("gamma", gamma_trace, path_gamma_posterior)

	err_trace = model.get("err")
	plot_posterior("err", err_trace, path_err_posterior)

	toc(start_time)