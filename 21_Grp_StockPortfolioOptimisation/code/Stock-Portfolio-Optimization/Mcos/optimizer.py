from __future__ import division

from abc import ABC, abstractmethod
from typing import Dict, List

import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
from numpy.linalg import inv, pinv
from pypfopt.efficient_frontier import EfficientFrontier
from scipy.optimize import minimize
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples

# from mcos.covariance_transformer import cov_to_corr
from covariance_transformer import cov_to_corr


class AbstractOptimizer(ABC):

    @abstractmethod
    def allocate(self, mu: np.array, cov: np.array) -> np.array:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class MarkowitzOptimizer(AbstractOptimizer):

    def allocate(self, mu: np.array, cov: np.array) -> np.array:
        ef = EfficientFrontier(mu, cov)
        ef.max_sharpe()
        weights = ef.clean_weights()

        return np.array(list(weights.values()))

    @property
    def name(self) -> str:
        return 'markowitz'


class NCOOptimizer(AbstractOptimizer):

    def __init__(self, max_num_clusters: int = None, num_clustering_trials=10):
        self.max_num_clusters = max_num_clusters
        self.num_clustering_trials = num_clustering_trials

    @property
    def name(self) -> str:
        return 'NCO'

    def allocate(self, mu: np.array, cov: np.array) -> np.array:
        cov = pd.DataFrame(cov)

        if mu is not None:
            mu = pd.Series(mu.flatten())
            assert mu.size == cov.shape[0], 'mu and cov dimension must be the same size'

        # get correlation matrix
        corr = cov_to_corr(cov)

        # find the optimal partition of clusters
        clusters = self._cluster_k_means_base(corr)

        # calculate intra-cluster allocations by finding the optimal portfolio for each cluster
        intra_cluster_allocations = pd.DataFrame(0, index=cov.index, columns=clusters.keys())
        for cluster_id, cluster in clusters.items():
            cov_ = cov.loc[cluster, cluster].values
            mu_ = mu.loc[cluster].values.reshape(-1, 1) if mu is not None else None
            intra_cluster_allocations.loc[cluster, cluster_id] = self._get_optimal_portfolio(cov_, mu_)

        # reduce covariance matrix
        cov = intra_cluster_allocations.T.dot(np.dot(cov, intra_cluster_allocations))
        mu = intra_cluster_allocations.T.dot(mu) if mu is not None else None

        # calculate inter_cluster allocations on reduced covariance matrix
        inter_cluster_allocations = pd.Series(self._get_optimal_portfolio(cov, mu), index=cov.index)

        # final allocations are the dot-product of the intra-cluster allocations and the inter-cluster allocations
        return intra_cluster_allocations \
            .mul(inter_cluster_allocations, axis=1) \
            .sum(axis=1).values \
            .reshape(-1, 1) \
            .flatten()

    def _cluster_k_means_base(self, corr: np.array) -> Dict[int, int]:
        distance_matrix = ((1 - corr.fillna(0)) / 2.) ** .5
        silhouettes = pd.Series()

        max_num_clusters = self.max_num_clusters
        if max_num_clusters is None:
            # if the max number of clusters wasn't specified, declare it based on corr
            max_num_clusters = corr.shape[0] // 2

        for _ in range(self.num_clustering_trials):
            for i in range(2, max_num_clusters + 1):  # find optimal num clusters
                kmeans_ = KMeans(n_clusters=i, n_jobs=1, n_init=1, random_state=42)

                kmeans_ = kmeans_.fit(distance_matrix)
                silhouettes_ = silhouette_samples(distance_matrix, kmeans_.labels_)

                new_calc = silhouettes_.mean() / silhouettes_.std()
                old_calc = silhouettes.mean() / silhouettes.std()

                if np.isnan(old_calc) or new_calc > old_calc:
                    silhouettes, kmeans = silhouettes_, kmeans_

        clusters = {
            i: corr.columns[np.where(kmeans.labels_ == i)].tolist()
            for i in np.unique(kmeans.labels_)
        }  # cluster members

        return clusters

    def _get_optimal_portfolio(self, cov: np.array, mu: np.array) -> np.array:

        try:
            inv = np.linalg.inv(cov)
        except np.linalg.LinAlgError:  # get the pseudo-inverse if the matrix is singular
            inv = np.linalg.pinv(cov)

        ones = np.ones(shape=(inv.shape[0], 1))

        if mu is None:
            mu = ones

        w = np.dot(inv, mu)
        w /= np.dot(ones.T, w)
        return w.flatten()


class HRPOptimizer(AbstractOptimizer):
    

    def allocate(self, mu: np.array, cov: np.array) -> np.array:
       
        corr = cov_to_corr(cov)

        dist = self._correlation_distance(corr)

        link = sch.linkage(dist, 'single')  # this step also calculates the Euclidean distance of 'dist'

        sorted_indices = self._quasi_diagonal_cluster_sequence(link)
        ret = self._hrp_weights(cov, sorted_indices)
        if ret.sum() > 1.001 or ret.sum() < 0.999:
            raise ValueError("Portfolio allocations don't sum to 1.")

        return ret

    @property
    def name(self) -> str:
        return 'HRP'

    def _inverse_variance_weights(self, cov: np.ndarray) -> np.ndarray:
        # Compute the inverse-variance portfolio
        ivp = 1. / np.diag(cov)
        ivp /= ivp.sum()
        return ivp

    def _cluster_sub_sequence(self, clustering_data: pd.DataFrame, combined_node: int) -> List:
        # recurisvely extracts the list of cluster indices that that belong to the children of combined_node
        row = clustering_data[clustering_data['combined_node'] == combined_node]
        if row.empty:
            return [combined_node]

        return self._cluster_sub_sequence(clustering_data, row.iloc[0]['node1']) + \
               self._cluster_sub_sequence(clustering_data, row.iloc[0]['node2'])

    def _quasi_diagonal_cluster_sequence(self, link: np.ndarray) -> List:
        # Sort clustered items by distance
        num_items = link[-1, 3].astype('int')
        clustering_data = pd.DataFrame(link[:, 0:2].astype('int'), columns=['node1', 'node2'])
        clustering_data['combined_node'] = clustering_data.index + num_items
        return self._cluster_sub_sequence(clustering_data, clustering_data.iloc[-1]['combined_node'])

    def _cluster_var(self, cov: np.ndarray) -> np.ndarray:
        # calculates the overall variance assuming the inverse variance portfolio weights of the constituents
        w_ = self._inverse_variance_weights(cov).reshape(-1, 1)
        return np.dot(np.dot(w_.T, cov), w_)[0, 0]

    def _hrp_weights(self, cov: np.ndarray, sorted_indices: List) -> np.ndarray:
     
        if len(sorted_indices) == 0:
            raise ValueError('sorted_indices is empty')

        if len(sorted_indices) == 1:
            return np.array([1.])

        split_indices = np.array_split(np.array(sorted_indices), 2)

        left_var = self._cluster_var(cov[:, split_indices[0]][split_indices[0]])
        right_var = self._cluster_var(cov[:, split_indices[1]][split_indices[1]])

        alloc_factor = 1. - left_var / (left_var + right_var)

        return np.concatenate([
            np.multiply(self._hrp_weights(cov, split_indices[0]), alloc_factor),
            np.multiply(self._hrp_weights(cov, split_indices[1]), 1. - alloc_factor)
        ])

    def _correlation_distance(self, corr: np.ndarray) -> np.ndarray:
        # A distance matrix based on correlation, where 0<=d[i,j]<=1
        # This is a proper distance metric
        dist = np.sqrt((1. - corr) / 2.)
        for i in range(dist.shape[0]):
            dist[i, i] = 0.  # diagonals should always be 0, but sometimes it's only close to 0
        return dist


class RiskParityOptimizer(AbstractOptimizer):

    def __init__(self, target_risk: np.array = None):
        self.target_risk = target_risk

    def allocate(self, mu: np.array, cov: np.array) -> np.array:

        if self.target_risk is None:
            target_risk = [1 / len(cov[0])] * len(cov[0])
        else:
            target_risk = self.target_risk

        ret = self._rp_weights(cov, target_risk)
        return ret

    @property
    def name(self) -> str:
        return 'Risk Parity'

    # risk budgeting optimization
    def _calculate_portfolio_var(self, w: np.array, cov: np.array) -> float:
        # function that calculates portfolio risk
        w = np.array(w, ndmin=2)
        return (w @ cov @ w.T)[0, 0]

    def _calculate_risk_contribution(self, w: np.array, cov: np.array) -> np.ndarray:
        # function that calculates asset contribution to total risk
        w = np.array(w, ndmin=2)
        sigma = np.sqrt(self._calculate_portfolio_var(w, cov))
        # Marginal Risk Contribution
        MRC = cov @ w.T
        # Risk Contribution
        RC = np.multiply(MRC, w.T) / sigma
        return RC

    def _risk_budget_objective(self, x: np.ndarray, pars: List) -> float:
        # calculate portfolio risk
        cov, target_risk = pars # covariance table and risk target in percent of portfolio risk
        sig_p = np.sqrt(self._calculate_portfolio_var(x, cov))  # portfolio sigma
        risk_target = np.array(np.multiply(sig_p, target_risk), ndmin=2)
        asset_RC = self._calculate_risk_contribution(x, cov)
        J = sum(np.square(asset_RC - risk_target.T))[0]  # sum of squared error
        return J

    def _total_weight_constraint(self, x):
        return np.sum(x) - 1.0

    def _long_only_constraint(self, x):
        return x

    def _rp_weights(self, cov: np.array, target_risk: List):
        w0 = target_risk
        cons = ({'type': 'eq', 'fun': self._total_weight_constraint},
                {'type': 'ineq', 'fun': self._long_only_constraint})

        # changed disp to false to remove excess risk parity logging
        res = minimize(self._risk_budget_objective, w0, args=[cov, target_risk], method='SLSQP', constraints=cons,
                       options={'disp': False})
        w_rb = np.array(res.x)

        return w_rb
