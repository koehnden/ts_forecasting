import matplotlib.pyplot as plt
import scipy.stats as scs


def plot_forecast_interval(df_interval, actual, ts_name, figsize=(20, 8)):
    plt.figure(figsize=figsize)
    plt.style.use('bmh')
    plt.title('Forecast Interval Plot', fontsize=20)
    plt.grid(True)
    plt.scatter(actual.index, actual.values, label='Actual Values')
    plt.fill_between(df_interval.index, df_interval['lower'], df_interval['upper'], facecolor='blue', alpha=0.2,
                     label='Forecast Interval')
    plt.plot(df_interval.index, df_interval['yhat'], '--b', label='Predicted Values')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.ylabel(ts_name, fontsize=15)
    plt.legend(loc='best', fontsize=15)


def gaussian_confidence_bands(yhat, sigma_hat, alpha):
    z_value = scs.norm.ppf(alpha)
    upper = yhat + z_value*sigma_hat
    lower = yhat - z_value*sigma_hat
    return lower.clip(0), upper
