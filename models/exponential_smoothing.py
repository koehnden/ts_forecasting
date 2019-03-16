import math
import numpy as np


def forecast_stderrors(model_fit, seasonal_periods, steps=1):
    """
   Analytical Forecast Standarderror estimates for Exponential Smoothing. Note that estimates depend on the used
   forecast_model_parameter combination, e.g. analytical variance of ES with additive trend is different ES with
   additive trend and additive seasonality.
   Formulas for estimates are taken from Hyndman, R.J., & Athanasopoulos, G. (2018) Forecasting: principles and practice).
   The code also largely follows their math notation, e.g. m are the seasonal_periods etc.
   So far this function only implements the estimate for ES with additive trend and ES with additive Trend and
   additive Seasonality.

   :param model_fit: HoltWinterResults Object return by the fit() function
   :param seasonal_periods: period of the seasonality, e.g. daily seasonality on hourly data than seasonal_period=24
   :param steps: forecast horizon
   :return: a forecast standard error for a single prediction step
   """
    variance_residuals = np.var(model_fit.resid)
    variance_forecast = 1 + (steps - 1)
    variance_forecast = add_variable_variance_term(variance_forecast, model_fit.params, seasonal_periods,
                                                   steps)
    variance_forecast *= variance_residuals
    return np.sqrt(variance_forecast)


def add_variable_variance_term(variance_forecast, model_coefficients, seasonal_periods, steps):
    alpha, beta, gamma = extract_fit_params_for_variance_estimation(model_coefficients)
    variance_forecast *= variance_additive_trend_component(alpha, beta, steps)
    variance_forecast += variance_additive_seasonality_component(alpha, beta, gamma, seasonal_periods, steps)
    return variance_forecast


def extract_fit_params_for_variance_estimation(model_coefficients):
    alpha = get_model_coefficient(model_coefficients, 'smoothing_level')
    beta = alpha * get_model_coefficient(model_coefficients, 'smoothing_slope')
    gamma = (1 - alpha) * get_model_coefficient(model_coefficients, 'smoothing_seasonal')
    return alpha, beta, gamma


def variance_additive_trend_component(alpha, beta, steps):
    return alpha ** 2 + alpha * beta * steps + 1.00 / 6.00 * beta ** 2 * steps * (2 * steps - 1)


def variance_additive_seasonality_component(alpha, beta, gamma, seasonal_periods, steps):
    if seasonal_periods:
        m = seasonal_periods
        k = int((steps - 1) / m)
    else:
        m, k = 0, 0
    return gamma * k * (2 * alpha + gamma + beta * m * (k + 1))


def get_forecast_model_param(param_dict, name, default_value=None):
    try:
        return param_dict[name]  # TODO: use get instead!
    except KeyError:
        return default_value


def get_model_coefficient(param_dict, name, default_value=0):
    try:
        param_value = param_dict[name]
    except KeyError:
        return default_value
    else:
        param_value = default_value if math.isnan(param_value) else param_value
        return param_value
