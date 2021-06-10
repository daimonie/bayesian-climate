import logging
import pymc3 as pm
import pandas as pd
import numpy as np


def bayes_mu_const_sigma(
    year,
    data,
    initial_mu_0=10,
    initial_mu_delta=2,
    min_year=1900,
    year_diff=120,
    initial_sigma=5,
    sample=10000
):
    with pm.Model() as model:
        mu_0 = pm.Normal("mu_0", mu=initial_mu_0, sigma=10, testval=0)
        mu_delta = pm.Normal("mu_delta", mu=initial_mu_delta, sigma=10, testval=0)

        observed = pm.Normal(
            "observed",
            mu=mu_0 + (year - min_year) * mu_delta / year_diff,
            sigma=initial_sigma,
            observed=data
        )

        start = pm.find_MAP()
        step = pm.NUTS()
        trace = pm.sample(sample, step=step, start=start)
        burned_trace = trace[int(sample*4/5):]

    return burned_trace

def generate_test_data(
    climate_change,
    year,
    initial_mu_0=10,
    initial_mu_delta=2,
    min_year=1900,
    year_diff=120,
    initial_sigma=5,
):
    test = []
    for t in year:
        mu = initial_mu_0 + climate_change * (t - min_year) / year_diff
        sigma = initial_sigma
        test.append(np.random.normal(mu, sigma, 1))
    test = np.array(test)[:,0]

    return test


def report_stats(x, name): 
    logging.info("{name} stats: min={min: .3f}, mean={mean: .3f}, max={max: .3f}, std={std: .3f}".format(
        name=name,
        min=np.min(x),
        mean=np.mean(x),
        max=np.max(x),
        std=np.std(x)
    ))