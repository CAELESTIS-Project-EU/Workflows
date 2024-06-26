# -*- coding: utf-8 -*-
from pycompss.api.task import task
from pycompss.api.parameter import *
import numpy as np
import pandas as pd
import itertools


# lee un txt llamado doe_seed.txt que contiene una linea por cada
# variable, en cada linea aparecen el minimo y maximo valor
# y un 0 para variables lineales, 1 para logaritmicas


@task(returns=1)
def sampling(sampler_input_file):
    casos = []
    with open(sampler_input_file, 'r') as f:
        fflvl = int(f.readline())
        for row in f:
            casos.append(row.split())
    casos = np.asarray(casos, dtype=float)
    X = np.zeros((len(casos), fflvl), float)
    ii = 0
    for entrada in casos:
        if entrada[2] == 0:
            X[ii] = np.linspace(entrada[0], entrada[1], fflvl)
        elif entrada[2] == 1:
            X[ii] = np.geomspace(entrada[0], entrada[1], fflvl)
        ii += 1

    number = 1
    i = 0
    X_fact = np.zeros((int(fflvl ** len(casos)), len(casos)), float)
    args = ()
    for ii in range(len(casos)):
        b = (X[ii, :])
        args += (b,)
    for combination in itertools.product(*args):
        X_fact[i, :] = (combination)
        i += 1
        number += 1
    return X_fact
    # np.savetxt('doe_file.txt', X_fact, ['%i','%i','%i','%i','%.4e'], delimiter = '\t')


@task(returns=1)
def from_doe(sampler_input_file):
    try:
        X_fact = pd.read_csv(sampler_input_file, delim_whitespace=True)
        return X_fact
    except Exception as e:
        raise ValueError(f"Error {e}")
