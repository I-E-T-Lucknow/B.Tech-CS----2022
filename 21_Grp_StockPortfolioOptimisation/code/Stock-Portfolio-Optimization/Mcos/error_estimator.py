import numpy as np
from abc import ABC, abstractmethod


class AbstractErrorEstimator(ABC):

    @abstractmethod
    def estimate(self, mu: np.array, cov: np.array, allocation: np.array, optimal_allocation: np.array) -> float:
        pass


class ExpectedOutcomeErrorEstimator(AbstractErrorEstimator):
    """Error Estimator that calculates the mean difference in expected outcomes"""

    def estimate(self, mu: np.array, cov: np.array, allocation: np.array, optimal_allocation: np.array) -> float:
        return _mean_difference_expected_outcome(optimal_allocation, allocation, mu)


class VarianceErrorEstimator(AbstractErrorEstimator):
    """Error Estimator that calculates the mean difference in variance"""

    def estimate(self, mu: np.array, cov: np.array, allocation: np.array, optimal_allocation: np.array) -> float:
        return _mean_difference_variance(cov, allocation, optimal_allocation)


class SharpeRatioErrorEstimator(AbstractErrorEstimator):
    """Error estimator that calculates the mean difference in Sharpe ratio"""

    def estimate(self, mu: np.array, cov: np.array, allocation: np.array, optimal_allocation: np.array) -> float:
        mean_difference_expected_outcome = _mean_difference_expected_outcome(optimal_allocation, allocation, mu)
        mean_difference_variance = _mean_difference_variance(cov, allocation, optimal_allocation)
        return mean_difference_expected_outcome / np.sqrt(mean_difference_variance)


def _mean_difference_expected_outcome(optimal_allocation: np.array, allocation: np.array, mu: np.array) -> float:
    return np.dot(optimal_allocation - allocation, mu)


def _mean_difference_variance(cov: np.array, allocation: np.array, optimal_allocation: np.array) -> float:
    return np.dot(optimal_allocation - allocation, np.dot(cov, optimal_allocation - allocation))
