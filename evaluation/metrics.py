import numpy as np
from sklearn import metrics


def print_relevant_metrics(y, yhat, model_name, prices):
    if model_name:
        print('-----------------------{}: Evaluation on y set ----------------------------------'.format(model_name))
    else:
        print('------------------------------ Evaluation on Test set ----------------------------------')
    print('Count of Overstocked items: {}'.format(count_overstock(y, yhat)))
    print('Count of Understocked items: {}'.format(count_understock(y, yhat)))
    print('Total_Value of Understocked Items: {}'.format(total_value_understock(y, yhat, prices=prices)))
    print('Estimated Monetary Costs: {}'.format(monetary_model_cost(y, yhat, prices, product_margin=0.1, overstock_costs=1)))
    print('Under/Overstocking Balance Loss: {}'.format(under_overstock_balance_loss(y, yhat, understock_costs=10, overstock_costs=1)))
    print_standard_regression_metrics(y, yhat)


def monetary_model_cost(y, yhat, prices, product_margin=0.75, overstock_costs=1):
    """
    Aims to calculate the monetary loss to of a model. I assume that understock is a much bigger concern.
    This takes also into account the selling price. I don't know the real margin of each product (useful data!).
    Therefore I assume that you earn net returns are 50% of the selling price (might be total wrong?).
    Furthermore, cost of stocking an item are unknown (also useful data/ I assume 1 here).
    Given stock cost and product margin we could build a realistic business metric for the model!
    :param y:
    :param yhat:
    :param prices:
    :param product_margin:
    :param overstock_costs:
    :return:
    """
    net_returns = product_margin * prices
    understock_loss = total_value_understock(y, yhat, net_returns)
    overstock_loss = count_overstock(y, yhat) * overstock_costs
    return understock_loss + overstock_loss


def under_overstock_balance_loss(y, yhat, understock_costs=10, overstock_costs=1):
    understock_loss = count_understock(y, yhat) * understock_costs
    overstock_loss = count_overstock(y, yhat) * overstock_costs
    return understock_loss + overstock_loss


def count_overstock(y, yhat):
    idx_overstock = np.where(yhat > y)[0]
    return (yhat[idx_overstock] - y[idx_overstock]).sum()


def count_understock(y, yhat):
    idx_understock = np.where(yhat < y)[0]
    return (y[idx_understock] - yhat[idx_understock]).sum()


def total_value_understock(y, yhat, prices):
    idx_understock = np.where(yhat < y)[0]
    understock = (y[idx_understock] - yhat[idx_understock])
    return (understock * prices[idx_understock]).sum()


def print_standard_regression_metrics(y, yhat):
    mae = metrics.mean_absolute_error(y, yhat)
    median_avg_error = metrics.median_absolute_error(y, yhat)
    mse = metrics.mean_squared_error(y, yhat)
    rmse = np.sqrt(mse)
    r2 = metrics.r2_score(y, yhat)
    print('MSE: {}'.format(mse))
    print('RMSE: {}'.format(rmse))
    print('Median Absolut Error {}'.format(median_avg_error))
    print('MAP: {}'.format(mae))
    print('R2: {}'.format(r2))
