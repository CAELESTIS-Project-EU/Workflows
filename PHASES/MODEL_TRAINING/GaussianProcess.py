from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.datasets import make_regression
from dislib.model_selection import GridSearchCV
import dislib as ds
import importlib
import pandas as pd
import numpy as np


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
    searcher = GridSearchCV(gpr, params)
    print("SHAPES")
    print(x.shape)
    print(y.shape)
    x = ds.array(x, block_size=x.shape)
    y = np.array(y)
    y = y[:, np.newaxis]
    y = ds.array(y, block_size=y.shape)
    print("SHAPES after")
    print(x.shape)
    print(y.shape)
    searcher.fit(x, y)
    return pd.DataFrame(searcher.cv_results_)[["params", "mean_test_score"]]


