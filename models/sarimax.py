import itertools
import warnings
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX


def order_selection(train, test, params, loss_func=mean_squared_error, **loss_kwargs):
    warnings.filterwarnings("ignore") # to ignore statsmodels warning for unconverged models
    best_score, best_cfg = float("inf"), None
    keys, values = zip(*params.items())
    grid = [dict(zip(keys, v)) for v in itertools.product(*values)]
    for params in grid:
        try:
            model_fit = SARIMAX(train, **params).fit()
        except:
            continue
        else:
            yhat = model_fit.forecast(test.shape[0])
            loss = loss_func(test, yhat, **loss_kwargs)

        if loss < best_score:
            best_score, best_params = loss, params
            print(best_score)

    print('Best ARIMA%s Loss=%.3f' % (best_params, best_score))
    return best_params, best_score
