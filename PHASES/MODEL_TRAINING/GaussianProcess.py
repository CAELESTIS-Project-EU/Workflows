import pickle
from sklearn.gaussian_process import GaussianProcessRegressor
from dislib.model_selection import GridSearchCV
import dislib as ds
import pandas as pd
import numpy as np


@task(returns=1)
def training(**kwargs):
    train_args = kwargs.get("args")
    return gen_model(train_args, **kwargs)


def gen_model(train_args, **kwargs):
    kernel = get_value(train_args, "kernel")
    results_folder = get_value(train_args, "results_folder")
    gpr = GaussianProcessRegressor()
    try:
        alpha = float(get_value(train_args, "alpha"))
    except:
        alpha = float("1e-10")
    x = get_value(train_args, "x")
    if isinstance(x, str):
        x = np.load(x)
    y = get_value(train_args, "y")
    if isinstance(x, str):
        y = np.load(y)
    params = {"kernel": kernel, "random_state": [0], "alpha": [alpha]}
    # use grid search with your training data (it might take a while, be patient)
    searcher = GridSearchCV(gpr, params, cv=5)
    x = ds.array(x, block_size=x.shape)
    y = np.array(y)
    y = y[:, np.newaxis]
    y = ds.array(y, block_size=y.shape)
    searcher.fit(x, y)
    write_file(results_folder, searcher, train_args)
    save_model(results_folder, pd.DataFrame(searcher.cv_results_)[["params", "mean_test_score"]], train_args)
    return


def write_file(output_folder, res, train_args, **kwargs):
    model_output = get_value(train_args, "model_output")
    # Initialize file_path to None
    file_path = None
    # Iterate over each dictionary in the list
    for item in model_output:
        if "path" in item:
            file_path = item["path"]
            break  # Stop the loop once the path is found
    # Check if file_path was found
    if file_path is not None:
        # You can now use file_path for further processing
        file = str(file_path)
        model_file = output_folder + "/" + file
        write(model_file, res)
    return


def write(file, res):
    with open(file, 'w') as f3:
        f3.write("MODEL RES: \n")
        f3.write(str(res))
        f3.close()
    return


def save_model(output_folder, model, train_args, **kwargs):
    model_dump = get_value(train_args, "model_dump")
    # Initialize file_path to None
    file_path = None
    # Iterate over each dictionary in the list
    for item in model_dump:
        if "path" in item:
            file_path = item["path"]
            break  # Stop the loop once the path is found
    # Check if file_path was found
    if file_path is not None:
        file = str(file_path)
        model_file = output_folder + "/" + file + ".pk1"
        save(model, model_file)
    return


def save(model, file):
    pickle.dump(model, open(file, 'wb'))
    return


def get_value(element, param):
    if param in element:
        return element[param]
    else:
        raise ValueError(f"The key '{param}' was not found in the dictionary.")
