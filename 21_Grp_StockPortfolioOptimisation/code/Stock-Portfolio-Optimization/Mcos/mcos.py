import numpy as np
import pandas as pd
from typing import List

from covariance_transformer import AbstractCovarianceTransformer
from error_estimator import AbstractErrorEstimator
from observation_simulator import AbstractObservationSimulator, MuCovLedoitWolfObservationSimulator, \
    MuCovObservationSimulator, MuCovJackknifeObservationSimulator
from optimizer import AbstractOptimizer
from utils import convert_price_history


def simulate_optimizations(
        obs_simulator: AbstractObservationSimulator,
        n_sims: int,
        optimizers: List[AbstractOptimizer],
        error_estimator: AbstractErrorEstimator,
        covariance_transformers: List[AbstractCovarianceTransformer]
) -> pd.DataFrame:
    error_estimates = {optimizer.name: [] for optimizer in optimizers}

    for i in range(n_sims):
        mu_hat, cov_hat = obs_simulator.simulate()

        for transformer in covariance_transformers:
            cov_hat = transformer.transform(cov_hat, obs_simulator.n_observations)

        for optimizer in optimizers:
            allocation = optimizer.allocate(mu_hat, cov_hat)
            optimal_allocation = optimizer.allocate(obs_simulator.mu, obs_simulator.cov)

            estimation = error_estimator.estimate(obs_simulator.mu, obs_simulator.cov, allocation, optimal_allocation)
            error_estimates[optimizer.name].append(estimation)

    return pd.DataFrame([
        {
            'optimizer': optimizer.name,
            'mean': np.mean(error_estimates[optimizer.name]),
            'stdev': np.std(error_estimates[optimizer.name])
        } for optimizer in optimizers
    ]).set_index('optimizer')


def simulate_optimizations_from_price_history(
        price_history: pd.DataFrame,
        simulator_name: str,
        n_observations:int,
        n_sims: int,
        optimizers: List[AbstractOptimizer],
        error_estimator: AbstractErrorEstimator,
        covariance_transformers: List[AbstractCovarianceTransformer]):

    mu, cov = convert_price_history(price_history)

    if simulator_name.lower() == "mucovledoitwolf":
        sim = MuCovLedoitWolfObservationSimulator(mu, cov, n_observations)
    elif simulator_name.lower() == "mucov":
        sim = MuCovObservationSimulator(mu, cov, n_observations)
    elif simulator_name.lower() == "jackknife":
        sim = MuCovJackknifeObservationSimulator(mu, cov, n_observations)
    else:
        raise ValueError("Invalid observation simulator name")

    return simulate_optimizations(sim, n_sims, optimizers, error_estimator, covariance_transformers)
