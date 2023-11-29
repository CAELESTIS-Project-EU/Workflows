from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.datasets import make_regression
from pycompss.api.api import compss_wait_on
from dislib.model_selection import GridSearchCV
import dislib as ds
import importlib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def training(x,y, training, **kwargs):
    # outputs = kwargs.get("outputs")
    # input = kwargs.get("input")
    # x = float(input.get("x"))
    # y = float(input.get("y"))
    res= gen_model(x, y, training)
    return res


def gen_parameters(kernel_type, **kwargs):
    module = importlib.import_module('PHASES.MODEL_TRAINING.PARAMETERS.' + kernel_type)
    return getattr(module, 'gen_param')(**kwargs)


def gen_model(x, y, training):
    kernel_type = training['kernel']['name']
    parameters = training['kernel']['parameters']
    gpr = GaussianProcessRegressor()
    # gpr.kernel = gen_parameters(kernel_type, parameters=parameters)
    # gpr.random_state = 0
    params = {"kernel": [gen_parameters(kernel_type, parameters=parameters)], "random_state": [0]}
    # use grid search with your training data (it might take a while, be patient)
    searcher = GridSearchCV(gpr, params, cv=2, scoring=mean_squared_error)
    print("SHAPES")
    print(x.shape, flush=True)
    x = ds.array(x, block_size=x.shape)
    y = np.array(y)
    y = y[:, np.newaxis]
    y = ds.array(y, block_size=y.shape)
    print("SHAPES after")
    print(x.shape, flush=True)
    print(y.shape, flush=True)
    print(compss_wait_on(x._blocks), flush=True)
    print(x.collect(), flush=True)
    print(compss_wait_on(y._blocks), flush=True)
    print(y.collect(), flush=True)
    searcher.fit(x, y)
    print(pd.DataFrame(searcher.cv_results_)[["params", "mean_test_score"]], flush=True)
    return pd.DataFrame(searcher.cv_results_)[["params", "mean_test_score"]]


