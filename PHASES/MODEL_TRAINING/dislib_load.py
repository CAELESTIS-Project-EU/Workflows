import dislib as ds
import numpy as np
import os
from pycompss.api.task import task
from pycompss.api.parameter import *


def load_twinkle(**kwargs):
    var_results = kwargs.get("var_results")
    input_file = kwargs.get("input_file")
    results_folder= kwargs.get("results_folder")
    num_columns_y=len(var_results)
    if num_columns_y is None or input_file is None or results_folder is None:
        raise ValueError("Required parameters are missing")
    else:
        return extract_outlayers_values(input_file, num_columns_y, results_folder)


@task(returns=1)
def load(**kwargs):
    inputFileX = kwargs.get("inputFileX")
    inputFileY = kwargs.get("inputFileY")
    if inputFileX is None or inputFileY is None:
        return get_from_numpy(kwargs.get("inputFileX"), kwargs.get("inputFileY"))


def get_from_numpy(inputFileX, inputFileY):
    X = np.load(inputFileX)
    Y = np.load(inputFileY)
    X = ds.array(X, block_size=X.shape)
    Y = Y[:, np.newaxis]
    Y = ds.array(Y, block_size=Y.shape)
    return X, Y




def extract_outlayers_values(input_file, num_columns_y, results_folder):
    data = np.loadtxt(input_file, skiprows = 1, delimiter = ';')
    with open(input_file, 'r') as f:
        headers = f.readline().split(';')
        # h2 = f.readline()
    headers[-1] = headers[-1].replace('\n','')
    n_outs = num_columns_y
    n_inps = len(data[0]) - n_outs
    data_lo = np.zeros([n_inps,len(data[0])])
    data_hi = np.zeros([n_inps,len(data[0])])
    for column in range(n_inps):
        data_lo[column] = data[data[:,column] == np.min(data[:,column])][0]
        data_hi[column] = data[data[:,column] == np.max(data[:,column])][0]
    data_xtr = np.r_[data_hi, data_lo]
    data_xtr2 = np.unique(data_xtr,axis = 0)
    data2 = []
    for row in data:
        if not np.any(np.all(data_xtr2 == row, axis=1)):
            data2.append(row)
    data2 = np.asarray(data2, dtype = float)

    np.savetxt(os.path.join(results_folder,'max_min_file.csv'), data_xtr2, delimiter = ';', header = ';'.join(headers), comments = '') #datos1e9mrg0.csv
    np.savetxt(os.path.join(results_folder, 'eval_file.csv'), data2, delimiter = ';', header = ';'.join(headers), comments = '') #datos1e9mrg1.csv
    X = data2[:, :n_inps]
    Y = data2[:, -num_columns_y:]

    X = ds.array(X, block_size=X.shape)
    Y = ds.array(Y, block_size=Y.shape)
    print(f"shape load X: {X}")
    print(f"shape load Y: {Y}")
    return X, Y