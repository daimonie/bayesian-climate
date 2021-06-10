import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from bayesian_climate.pipes import parse_datetime
from bayesian_climate.utils import setup_log

if __name__ == "__main__":
	setup_log(name='bayes')
	logging.info("Logging has been setup.")


	sns.set_theme(color_codes=True)

	df_raw = pd.read_csv(
	        'raw_data.csv',
	        sep=',',
	        header=2
	    )

	df_raw.head()

	df_long = (
	    pd.melt(
	        df_raw,
	        id_vars=["jaar"],
	        value_vars=["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"],
	    )
	    .assign(
	        year=lambda d: [int(_) for _ in d.jaar.values],
	        month=lambda d: d.variable,
	        temp=lambda d: d.value
	    )
	    .assign(
	        date=lambda d: [parse_datetime(d.year[i], d.month[i]) for i in range(len(d))]
	    )
	    .drop(columns=['jaar', 'variable', 'value'])
	)

	df_long.head()

	plt.figure(figsize=(25,4))
	sns.lineplot(data=df_long, x='date', y='temp')
	plt.show()

	plt.figure(figsize=(25,4))
	sns.lineplot(data=df_long, x='date', y='temp', hue="month")
	plt.show()
	df_year = (
	    df_long
	    .groupby(by='year')
	    .agg({
	        'temp': np.mean
	    })
	    .reset_index()
	)
	df_year.head()
	plt.figure(figsize=(25,4))
	sns.regplot(data=df_year, x='year', y='temp')
	plt.show() 