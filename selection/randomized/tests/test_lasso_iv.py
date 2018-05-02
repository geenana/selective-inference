import numpy as np

import selection.randomized.lasso as L; reload(L)
from selection.randomized.lasso_iv import lasso_iv, lasso_iv_ar
import matplotlib.pyplot as plt
from statsmodels.distributions import ECDF

################################################################################

#  test file for lasso_iv class

# include the screening in here

################################################################################

# if true_model is True, Sigma_12 is the true Sigma_{12}
# otherwise Sigma_12 will be the consistent estimator
def test_lasso_iv_instance(n=1000, p=10, s=3, ndraw=5000, burnin=5000, true_model=True, Sigma_12=0.8, gsnr_invalid=1., gsnr_valid=1., beta_star=1.):

    Z, D, Y, alpha, beta_star, gamma = lasso_iv.bigaussian_instance(n=n,p=p,s=s, gsnr_invalid=gsnr_invalid, gsnr_valid=gsnr_valid, beta=beta_star,Sigma=np.array([[1., Sigma_12],[Sigma_12, 1.]]))

    conv = lasso_iv(Y, D, Z)
    conv.fit()

    if true_model is True:
        sigma_11 = 1.
    else:
        sigma_11 = conv.estimate_covariance()

    pivot = None
    interval = None
    if set(np.nonzero(alpha)[0]).issubset(np.nonzero(conv._overall)[0]) and conv._inactive.sum()>0:
        pivot, _, interval = conv.summary(parameter=beta_star, Sigma_11=sigma_11)
    return pivot, interval

def test_pivots(nsim=500, n=1000, p=10, s=3, ndraw=5000, burnin=5000, true_model=True, Sigma_12=0.8, gsnr_invalid=1., gsnr_valid=1., beta_star=1.):
    P0 = []
    #intervals = []
    coverages = []
    lengths = []
    for i in range(nsim):
        p0, interval = test_lasso_iv_instance(n=n, p=p, s=s, true_model=true_model, Sigma_12=Sigma_12, gsnr_invalid=gsnr_invalid, gsnr_valid=gsnr_valid, beta_star=beta_star)
        if p0 is not None and interval is not None:
            P0.extend(p0)
            #intervals.extend(interval)
            coverages.extend([(interval[0][0] < beta_star) * (interval[0][1] > beta_star)])
            lengths.extend([interval[0][1] - interval[0][0]])

    print('pivots', np.mean(P0), np.std(P0), np.mean(np.array(P0) < 0.05))
    print('confidence intervals', np.mean(coverages), np.mean(lengths))

    #U = np.linspace(0, 1, 101)
    #plt.plot(U, ECDF(P0)(U))
    #plt.plot(U, U, 'k--')
    #plt.show()

    return P0


# if true_model is True, Sigma_12 is the true Sigma_{12}
# otherwise Sigma_12 will be the consistent estimator
def test_lasso_iv_ar_instance(n=1000, p=10, s=3, ndraw=5000, burnin=5000, true_model=True, Sigma_12=0.8, gsnr_invalid=1., gsnr_valid=1., beta_star=1.):

    Z, D, Y, alpha, beta_star, gamma = lasso_iv_ar.bigaussian_instance(n=n,p=p,s=s, gsnr_invalid=gsnr_invalid, gsnr_valid=gsnr_valid, beta=beta_star,Sigma=np.array([[1., Sigma_12],[Sigma_12, 1.]]))

    conv = lasso_iv_ar(Y, D, Z)
    conv.fit()

    if true_model is True:
        sigma_11 = 1.
    else:
        sigma_11 = conv.estimate_covariance()

    pivot = None
    interval = None
    if set(np.nonzero(alpha)[0]).issubset(np.nonzero(conv._overall)[0]) and conv._inactive.sum()>0:
        pivot, _, interval = conv.summary(parameter=beta_star, Sigma_11=sigma_11)
    return pivot, interval

def test_pivots_ar(nsim=500, n=1000, p=10, s=3, ndraw=5000, burnin=5000, true_model=True, Sigma_12=0.8, gsnr_invalid=1., gsnr_valid=1., beta_star=1.):
    P0 = []
    #intervals = []
    #coverages = []
    #lengths = []
    for i in range(nsim):
        p0, interval = test_lasso_iv_ar_instance(n=n, p=p, s=s, true_model=true_model, Sigma_12=Sigma_12, gsnr_invalid=gsnr_invalid, gsnr_valid=gsnr_valid, beta_star=beta_star)
        #if p0 is not None and interval is not None:
        if p0 is not None:
            P0.extend(p0)
            #intervals.extend(interval)
            #coverages.extend([(interval[0][0] < beta_star) * (interval[0][1] > beta_star)])
            #lengths.extend([interval[0][1] - interval[0][0]])

    print('pivots', np.mean(P0), np.std(P0), np.mean(np.array(P0) < 0.05))
    #print('confidence intervals', np.mean(coverages), np.mean(lengths))

    #U = np.linspace(0, 1, 101)
    #plt.plot(U, ECDF(P0)(U))
    #plt.plot(U, U, 'k--')
    #plt.show()

    return P0



# Sigma_12 is the true Sigma_{12}
def test_stat_lasso_iv_instance(n=1000, p=10, s=3, ndraw=5000, burnin=5000, Sigma_12=0.8, gsnr=1., beta_star=1.):

    #inst, const = bigaussian_instance, lasso_iv
    Z, D, Y, alpha, beta_star, gamma = lasso_iv.bigaussian_instance(n=n,p=p,s=s, gsnr=gsnr,beta=beta_star,Sigma=np.array([[1., Sigma_12],[Sigma_12, 1.]]))

    #n, p = Z.shape

    conv = stat_lasso_iv(Y, D, Z)
    conv.fit()

    if set(np.nonzero(alpha)[0]).issubset(np.nonzero(conv._overall)[0]) and conv._inactive.sum()>0:
        pivot, _, _ = conv.summary(parameter=beta_star)
    return pivot

def test_pivots_stat(nsim=500, n=1000, p=10, s=3, ndraw=5000, burnin=5000, Sigma_12=0.8, gsnr=1., beta_star=1.):
    P0 = []
    for i in range(nsim):
        try:
            p0 = test_stat_lasso_iv_instance(n=n, p=p, s=s, Sigma_12=Sigma_12, gsnr=gsnr, beta_star=beta_star)
        except:
            p0 = []
        P0.extend(p0)

    print(np.mean(P0), np.std(P0), np.mean(np.array(P0) < 0.05))

    U = np.linspace(0, 1, 101)
    plt.plot(U, ECDF(P0)(U))
    plt.plot(U, U, 'r--')
    plt.show()


def main(nsim=500):

    P0 = []
    from statsmodels.distributions import ECDF

    n, p, s = 1000, 10, 3
    Sigma_12 = 0.8
    gsnr = 1.
    beta_star = 1.

    for i in range(nsim):
        try:
            p0 = test_lasso_iv_instance(n=n, p=p, s=s, Sigma_12=Sigma_12, gsnr=gsnr, beta_star=beta_star)
        except:
            p0 = []
        P0.extend(p0)

    print(np.mean(P0), np.std(P0), np.mean(np.array(P0) < 0.05))

    U = np.linspace(0, 1, 101)
    #plt.clf()
    plt.plot(U, ECDF(P0)(U))
    plt.plot(U, U, 'r--')
    #plt.savefig("plot.pdf")
    plt.show()


if __name__ == "__main__":
    main()
