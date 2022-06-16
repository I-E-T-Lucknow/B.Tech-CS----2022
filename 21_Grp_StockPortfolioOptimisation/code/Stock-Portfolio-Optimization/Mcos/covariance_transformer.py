from abc import ABC, abstractmethod
import numpy as np
from numpy import linalg
from sklearn.neighbors import KernelDensity
from scipy.optimize import minimize
import pandas as pd


def cov_to_corr(cov: np.array) -> np.array:
    std = np.sqrt(np.diag(cov))
    corr = cov / np.outer(std, std)
    corr[corr < -1], corr[corr > 1] = -1, 1  # numerical error
    return corr


def corr_to_cov(corr: np.array, std: np.array) -> np.array:
    cov = corr * np.outer(std, std)
    return cov


def reorder_matrix(m: np.array, sort_index: np.array) -> np.array:
    m = m[sort_index, :]
    m = m[:, sort_index]
    return m


class AbstractCovarianceTransformer(ABC):

    @abstractmethod
    def transform(self, cov: np.array, n_observations: int) -> np.array:

        pass


class DeNoiserCovarianceTransformer(AbstractCovarianceTransformer):
    def __init__(self, bandwidth: float = .25):
       
        self.bandwidth = bandwidth

    def transform(self, cov: np.array, n_observations: int) -> np.array:
    
        #  q=T/N where T=sample length and N=number of variables
        q = n_observations / cov.shape[1]

        # get correlation matrix based on covariance matrix
        correlation_matrix = cov_to_corr(cov)

        # Get eigenvalues and eigenvectors in the correlation matrix
        eigenvalues, eigenvectors = self._get_PCA(correlation_matrix)

        # Find max random eigenvalue
        max_eigenvalue = self._find_max_eigenvalue(np.diag(eigenvalues), q)

        # de-noise the correlation matrix
        n_facts = eigenvalues.shape[0] - np.diag(eigenvalues)[::-1].searchsorted(max_eigenvalue)
        correlation_matrix = self._de_noised_corr(eigenvalues, eigenvectors, n_facts)

        # recover covariance matrix from correlation matrix
        de_noised_covariance_matrix = corr_to_cov(correlation_matrix, np.diag(cov) ** .5)
        return de_noised_covariance_matrix

    def _get_PCA(self, matrix: np.array) -> (np.array, np.array):
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        indices = eigenvalues.argsort()[::-1]  # arguments for sorting eigenvalues desc
        eigenvalues, eigenvectors = eigenvalues[indices], eigenvectors[:, indices]
        eigenvalues = np.diagflat(eigenvalues)
        return eigenvalues, eigenvectors

    def _find_max_eigenvalue(self, eigenvalues: np.array, q: float) -> float:
        # Find max random eigenvalues by fitting Marcenko's dist to the empirical one
        out = minimize(
            lambda *x: self._err_PDFs(*x),
            .5,
            args=(eigenvalues, q),
            bounds=((1E-5, 1 - 1E-5),)
        )
        if out['success']:
            var = out['x'][0]
        else:
            var = 1
        max_eigenvalue = var * (1 + (1. / q) ** .5) ** 2
        return max_eigenvalue

    def _err_PDFs(self, var: float, eigenvalues: pd.Series, q: float, pts: int = 1000) -> float:
        # Fit error
        theoretical_pdf = self._mp_PDF(var, q, pts)  # theoretical probability density function
        empirical_pdf = self._fit_KDE(eigenvalues,
                                      x=theoretical_pdf.index.values)  # empirical probability density function
        sse = np.sum((empirical_pdf - theoretical_pdf) ** 2)
        return sse

    def _mp_PDF(self, var: float, q: float, pts: int) -> pd.Series:
        min_eigenvalue, max_eigenvalue = var * (1 - (1. / q) ** .5) ** 2, var * (1 + (1. / q) ** .5) ** 2
        eigenvalues = np.linspace(min_eigenvalue, max_eigenvalue, pts).flatten()
        pdf = q / (2 * np.pi * var * eigenvalues) * \
              ((max_eigenvalue - eigenvalues) * (eigenvalues - min_eigenvalue)) ** .5
        pdf = pdf.flatten()
        pdf = pd.Series(pdf, index=eigenvalues)
        return pdf

    def _fit_KDE(
            self,
            obs: np.array,
            kernel: str = 'gaussian',
            x: np.array = None
    ) -> pd.Series:
        if len(obs.shape) == 1:
            obs = obs.reshape(-1, 1)
        kde = KernelDensity(kernel=kernel, bandwidth=self.bandwidth).fit(obs)
        if x is None:
            x = np.unique(obs).reshape(-1, 1)
        if len(x.shape) == 1:
            x = x.reshape(-1, 1)
        log_prob = kde.score_samples(x)  # log(density)
        pdf = pd.Series(np.exp(log_prob), index=x.flatten())
        return pdf

    def _de_noised_corr(self, eigenvalues: np.array, eigenvectors: np.array, n_facts: int) -> np.array:
        # Remove noise from corr by fixing random eigenvalues
        eigenvalues_ = np.diag(eigenvalues).copy()
        eigenvalues_[n_facts:] = eigenvalues_[n_facts:].sum() / float(eigenvalues_.shape[0] - n_facts)
        eigenvalues_ = np.diag(eigenvalues_)
        corr = np.dot(eigenvectors, eigenvalues_).dot(eigenvectors.T)
        corr = cov_to_corr(corr)
        return corr


class DetoneCovarianceTransformer(AbstractCovarianceTransformer):
    def __init__(self, n_remove: int):
        self.n_remove = n_remove

    def transform(self, cov: np.array, n_observations: int) -> np.array:
        if self.n_remove == 0:
            return cov

        corr = cov_to_corr(cov)

        w, v = linalg.eig(corr)

        # sort from highest eigenvalues to lowest
        sort_index = np.argsort(-np.abs(w))  # get sort_index in descending absolute order - i.e. from most significant
        w = w[sort_index]
        v = v[:, sort_index]

        # remove largest eigenvalue component
        v_market = v[:, 0:self.n_remove]  # largest eigenvectors
        w_market = w[0:self.n_remove]

        market_comp = np.matmul(
            np.matmul(v_market, w_market).reshape((v.shape[0], self.n_remove,)),
            np.transpose(v_market)
        )

        c2 = corr - market_comp

        # normalize the correlation matrix so the diagonals are 1
        norm_matrix = np.diag(c2.diagonal() ** -0.5)
        c2 = np.matmul(np.matmul(norm_matrix, c2), np.transpose(norm_matrix))

        return corr_to_cov(c2, np.diag(cov) ** .5)
