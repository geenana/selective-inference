from __future__ import print_function
import numpy as np
import time
import regreg.api as rr
from selection.tests.instance import logistic_instance, gaussian_instance
from selection.randomized.M_estimator import M_estimator_split
from selection.bayesian.inference_rr_data_split import smooth_cube_barrier, selection_probability_split, map_credible_split


def test_sel_prob_split(n=100, p=20, s=5, snr=5, rho=0.1,lam_frac=1.,loss='gaussian'):

    X, y, beta, nonzero, sigma = gaussian_instance(n=n, p=p, s=s, rho=rho, snr=snr, sigma=1.)
    lagrange = lam_frac * np.mean(np.fabs(np.dot(X.T, np.random.standard_normal((n, 2000)))).max(0)) * sigma
    loss = rr.glm.gaussian(X, y)
    epsilon = 1. / np.sqrt(n)

    W = np.ones(p) * lagrange
    penalty = rr.group_lasso(np.arange(p),weights=dict(zip(np.arange(p), W)), lagrange=1.)

    total_size = loss.saturated_loss.shape[0]

    subsample_size = int(0.8* total_size)

    generative_mean = np.append(snr * np.ones(s), np.zeros(p - s))
    sel_split = selection_probability_split(loss, epsilon, penalty, generative_mean, subsample_size)
    nactive = sel_split ._overall.sum()

    active_set = np.asarray([i for i in range(p) if sel_split ._overall[i]])

    true_support = np.asarray([i for i in range(p) if i < s])

    print("active set, true_support", active_set, true_support)

    if (set(active_set).intersection(set(true_support)) == set(true_support)) == True:

        sel_prob_split = sel_split.minimize2(nstep=100)[::-1]
        print("sel prob and minimizer", sel_prob_split[0], (sel_prob_split[1])[p:])
        #sel_prob_grad = sel_split.smooth_objective_gradient_map(np.append(snr * np.ones(s), np.zeros(nactive - s)))
        #print("test gradient map",sel_prob_grad)

#test_sel_prob_split()

def grad_sel_split(n=100, p=20, s=5, snr=5, rho=0.1,lam_frac=1.,loss='gaussian'):

    X, y, beta, nonzero, sigma = gaussian_instance(n=n, p=p, s=s, rho=rho, snr=snr, sigma=1.)
    lagrange = lam_frac * np.mean(np.fabs(np.dot(X.T, np.random.standard_normal((n, 2000)))).max(0)) * sigma
    loss = rr.glm.gaussian(X, y)
    epsilon = 1. / np.sqrt(n)

    W = np.ones(p) * lagrange
    penalty = rr.group_lasso(np.arange(p),weights=dict(zip(np.arange(p), W)), lagrange=1.)

    total_size = loss.saturated_loss.shape[0]

    subsample_size = int(0.8* total_size)

    prior_variance = 100.

    grad_split = selective_grad_map_split(loss, epsilon, penalty, subsample_size, p, prior_variance)

    #active_set = np.asarray([i for i in range(p) if inf_split._overall[i]])

    #true_support = np.asarray([i for i in range(p) if i < s])

    #print("active set, true_support", active_set, true_support)

    #nactive = inf_split._overall.sum()

    #if (set(active_set).intersection(set(true_support)) == set(true_support)) == True:

    test = np.zeros(p)

    sel_grad = grad_split.smooth_objective(test, 'both')
        #sel_grad_0 = inf_split.smooth_objective_post(test)
        #print("grad of sel map", sel_grad_0)

        #sel_MAP = inf_split.map_solve(nstep=100)[::-1]

    print("grad of sel map",sel_grad)
        #print("sel prob and minimizer", sel_MAP[0], sel_MAP[1])

#grad_sel_split()

def test_sel_prob_split_new(n=100, p=20, s=5, snr=5, rho=0.1,lam_frac=1.):

    X, y, beta, nonzero, sigma = gaussian_instance(n=n, p=p, s=s, rho=rho, snr=snr, sigma=1.)
    lagrange = lam_frac * np.mean(np.fabs(np.dot(X.T, np.random.standard_normal((n, 2000)))).max(0)) * sigma
    loss = rr.glm.gaussian(X, y)
    epsilon = 1. / np.sqrt(n)

    W = np.ones(p) * lagrange
    penalty = rr.group_lasso(np.arange(p),weights=dict(zip(np.arange(p), W)), lagrange=1.)

    total_size = loss.saturated_loss.shape[0]

    subsample_size = int(0.8* total_size)

    prior_variance = 100.

    solver = M_estimator_split(loss, epsilon, subsample_size, penalty)

    solver.Msolve()

    active_set = np.asarray([i for i in range(p) if solver._overall[i]])

    true_support = np.asarray([i for i in range(p) if i < s])

    #generative_mean = np.append(snr * np.ones(s), np.zeros(p - s))

    print("active set, true_support", active_set, true_support)

    #sel_split = selection_probability_split(solver, generative_mean)

    test = solver.observed_opt_state[solver._overall]

    if (set(active_set).intersection(set(true_support)) == set(true_support)) == True:
        #sel_prob_split = sel_split.minimize2(nstep=100)[::-1]
        #print("sel prob and minimizer", sel_prob_split[0], (sel_prob_split[1])[p:])

        grad_split = map_credible_split(solver, prior_variance)
        sel_grad = grad_split.smooth_objective_post(test, 'both')

        print("value and gradient", sel_grad)


test_sel_prob_split_new()
