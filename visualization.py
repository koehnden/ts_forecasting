import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statistics.graphics.tsaplots import plot_acf, plot_pacf


def plot_forecast_interval(df_interval, actual, ts_name, ylim=None, figsize=(20, 8)):
    plt.figure(figsize=figsize)
    plt.style.use('bmh')
    plt.title('Forecast Interval Plot', fontsize=20)
    plt.grid(True)
    plt.scatter(actual.index, actual.values, label='Actual Values')
    plt.fill_between(df_interval.index, df_interval['lower'], df_interval['upper'], facecolor='blue', alpha=0.2,
                     label='Forecast Interval')
    plt.plot(df_interval.index, df_interval['yhat'], '--b')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.ylabel(ts_name, fontsize=15)
    plt.legend(loc='best', fontsize=15)


def plot_anomalies(df_corridor, mark_lower, mark_upper):
    if mark_lower:
        low_anomalies = df_corridor[df_corridor['actual_value'] < df_corridor['lower']]
        plt.scatter(low_anomalies.index, low_anomalies['actual_value'], color='hotpink')
    if mark_upper:
        high_anomalies = df_corridor[df_corridor['actual_value'] > df_corridor['upper']]
        plt.scatter(high_anomalies.index, high_anomalies['actual_value'], color='hotpink')


def ts_summary_plot(df_daily):
    df_daily_sold = df_daily['units_sold'].groupby(pd.Grouper(freq='D')).sum()

    plt.figure(figsize=(24,16))
    plt.subplot(2,2,1)
    plt.plot(df_daily_sold, '-b')
    plt.title('Units Sold')

    plt.subplot(2,2,2)
    plt.plot(df_daily[(df_daily['website'] == 1)]['units_sold'], '-b', label='website 1')
    plt.plot(df_daily[(df_daily['website'] == 2)]['units_sold'], '-r', label='website 2')
    plt.plot(df_daily[(df_daily['website'] == 3)]['units_sold'], '-g', label='website 3')
    plt.title('Units Sold per Website')
    plt.legend(loc='best', fontsize=15)

    fig, axs = plt.subplots(figsize=(24, 8), nrows=1, ncols=2)
    plot_pacf(df_daily_sold, lags=30, ax=axs[0])
    plot_acf(df_daily_sold, lags=30, ax=axs[1])
    plt.show()
