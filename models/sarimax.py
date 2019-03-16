import itertools
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from evaluation.metrics import under_overstock_balance_loss


def order_selection(train, test, params, loss_func=under_overstock_balance_loss, **loss_kwargs):
    warnings.filterwarnings("ignore") # to ignore statsmodels warning for unconverged models
    best_score, best_cfg = float("inf"), None
    keys, values = zip(*params.items())
    grid = [dict(zip(keys, v)) for v in itertools.product(*values)]
    for cfgs in grid:
        print(cfgs)
        order = (cfgs['ar_order'], cfgs['difference'], cfgs['ma_order'])
        seasonal_order = (cfgs['seasonal_ar'], cfgs['seasonal_difference'], cfgs['seasonal_ma'], cfgs['seasonal_periods'])
        try:
            model_fit = SARIMAX(train, order=order, seasonal_order=seasonal_order).fit()
            yhat = model_fit.forecast()
            loss = loss_func(test, yhat, **loss_kwargs)
            print(loss)
        except:
            continue

        if loss < best_score:
            best_score, best_cfg = loss, cfgs

    print('Best ARIMA%s Loss=%.3f' % (best_cfg, best_score))
    return best_cfg, best_score
