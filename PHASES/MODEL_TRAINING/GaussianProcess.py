from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.datasets import make_regression
from dislib.model_selection import GridSearchCV
import dislib as ds
import importlib
import pandas as pd


def training(training, **kwargs):
    #outputs = kwargs.get("outputs")
    #input = kwargs.get("input")
    #x = float(input.get("x"))
    #y = float(input.get("y"))
    x, y = make_regression(n_samples=5, n_features=2, noise=1, random_state=42)
    gen_model(x, y, training)
    return

def gen_parameters(kernel_type, **kwargs):
    module = importlib.import_module('PHASES.MODEL_TRAINING.PARAMETERS.' + kernel_type)
    return getattr(module, 'gen_param')(**kwargs)

def gen_model(x, y, training):
    kernel_type= training['kernel']['name']
    parameters= training['kernel']['parameters']
    gpr = GaussianProcessRegressor()
    #gpr.kernel = gen_parameters(kernel_type, parameters=parameters)
    #gpr.random_state = 0
    params= { "kernel" : [gen_parameters(kernel_type, parameters=parameters)], "random_state": [0]}
    # use grid search with your training data (it might take a while, be patient)
    searcher = GridSearchCV(gpr, params)
    x = ds.array(x)
    y = ds.array(y)
    searcher.fit(x, y)
    print("RESULT")
    print(pd.DataFrame(searcher.cv_results_)[["params", "mean_test_score"]])
