import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import theano.tensor as tt
import pymc3 as pm
from datetime import datetime
from bayesian_climate.pipes import parse_datetime
from bayesian_climate.utils import setup_log, savefig, startfig, stop
from bayesian_climate.model import bayes_mu_const_sigma, generate_test_data, report_stats
filenames = {
    "raw": 'data/raw_data.csv',
    "timeseries_simple": "figures/timeseries_simple.png",
    "timeseries_year": "figures/timeseries_year.png",
    "timeseries_month": "figures/timeseries_month.png",
    "test_data": "figures/test_data.png",
    "test_burned_trace": "figures/test_burned_trace.png",
    "burned_trace": "figures/burned_trace.png"
}


if __name__ == "__main__":
    setup_log(name='bayes')
    logging.info("Logging has been setup.")


    sns.set_theme(color_codes=True)

    df_raw = pd.read_csv(
            filenames['raw'],
            sep=',',
            header=2
        )

    logging.info(df_raw.head())


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
        .sort_values(by='date', ascending=True)
        .dropna()
        .reset_index()
        .drop(columns=['jaar', 'variable', 'value', 'index'])
    )

    logging.info(df_long.head(12))

    startfig()
    sns.lineplot(data=df_long, x='date', y='temp')
    savefig(filenames['timeseries_simple'])

    startfig()
    sns.lineplot(data=df_long, x='date', y='temp', hue="month")
    savefig(filenames['timeseries_month'])
    df_year = (
        df_long
        .groupby(by='year')
        .agg({
            'temp': np.mean
        })
        .reset_index()
    )
    logging.info(df_year.head())

    startfig()
    sns.regplot(data=df_year, x='year', y='temp')
    savefig(filenames['timeseries_year']) 
    logging.info("""

Initial exploration done. Let's pymc3 this.

The idea is that we want to see whether or not the parameters
change with time.

so, we will fit:
* sigma(t) = sigma_0 THIS IS NOT bayesian, but a const
* mu(t) = mu_0 + (year - min_year) * mu_delta / year_diff

where t is at a resolution of years

For simplicity, we assume that sigma does not change
with time. The initial parameters are:
- sigma = std(X))
- mu_0 = mean(X)
- mu_delta = 0

We assume each of these to be normally distributed around their initial values,
choosing the variance of each to be large (10 values).

If you're wondering why sigma isn't a bayesian parameter,
it's because I couldn't get it to work last night.
""")

    initial_mu_0 = 0.5*np.mean(df_long.temp.values[0:100])
    initial_sigma = np.std(df_long.temp.values[0:100])
    initial_mu_delta = np.mean(df_long.temp.values) - initial_mu_0

    year = df_long.year.values
    year_diff = (np.max(year) - np.min(year))
    min_year = np.min(year)

    temp = df_long.temp.values

    logging.info(f"Generating testing data, period {year_diff} years")
    climate_change = 2

    test = generate_test_data(
        climate_change,
        year,
        initial_mu_0=initial_mu_0,
        initial_mu_delta=initial_mu_delta,
        min_year=min_year,
        year_diff=year_diff,
        initial_sigma=initial_sigma,
    )

    report_stats(test, "Testing data")
    report_stats(temp, "Real data") 

    logging.info(f"""Starting with:
mu = {initial_mu_0: .3f} + {initial_mu_delta: .3f} * t
sigma = {initial_sigma: .3f}
    """)

    df_test = pd.DataFrame.from_dict({
        'year': year,
        'temp': test
        }) 

    startfig()
    plt.title("Testing data.")
    sns.regplot(data=df_test, x='year', y='temp')
    savefig(filenames['test_data']) 

   
    burned_trace = bayes_mu_const_sigma(
        year,
        test,
        initial_mu_0=initial_mu_0,
        initial_mu_delta=initial_mu_delta,
        min_year=min_year,
        year_diff=year_diff,
        initial_sigma=initial_sigma,
        sample=10000
    )
    startfig()
    plt.title("Testing burn trace.")
    pm.plot_trace(burned_trace)
    savefig(filenames['test_burned_trace']) 



    burned_trace = bayes_mu_const_sigma(
        year,
        temp,
        initial_mu_0=initial_mu_0,
        initial_mu_delta=initial_mu_delta,
        min_year=min_year,
        year_diff=year_diff,
        initial_sigma=initial_sigma,
        sample=100000
    )
    startfig()
    plt.title("Real burn trace.")
    pm.plot_trace(burned_trace)
    savefig(filenames['burned_trace']) 