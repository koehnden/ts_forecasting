import scipy.stats as scs


def gaussian_confidence_bands(yhat, sigma_hat, alpha):
    z_value = scs.norm.ppf(alpha)
    upper = yhat + z_value*sigma_hat
    lower = yhat - z_value*sigma_hat
    return lower.clip(0), upper
