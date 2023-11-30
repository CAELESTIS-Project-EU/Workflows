import pickle

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.datasets import make_regression
from pycompss.api.api import compss_wait_on
from dislib.model_selection import GridSearchCV
import dislib as ds
import importlib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error


def training(x, y, training, **kwargs):
    return gen_model(x, y, training)


def gen_parameters(kernel_type, **kwargs):
    module = importlib.import_module('PHASES.MODEL_TRAINING.PARAMETERS.' + kernel_type)
    return getattr(module, 'gen_param')(**kwargs)


def gen_model(x, y, training):
    kernel_type = training['kernel']['name']
    parameters = training['kernel']['parameters']
    gpr = GaussianProcessRegressor()
    # gpr.kernel = gen_parameters(kernel_type, parameters=parameters)
    # gpr.random_state = 0
    try:
        alpha = float(parameters['alpha'])
    except:
        alpha = float("1e-10")
    params = {"kernel": [gen_parameters(kernel_type, parameters=parameters)], "random_state": [0], "alpha": [alpha]}
    # use grid search with your training data (it might take a while, be patient)
    searcher = GridSearchCV(gpr, params, cv=5)
    x = ds.array(x, block_size=x.shape)
    y = np.array(y)
    y = y[:, np.newaxis]
    y = ds.array(y, block_size=y.shape)
    searcher.fit(x, y)
    return searcher, pd.DataFrame(searcher.cv_results_)[["params", "mean_test_score"]]

