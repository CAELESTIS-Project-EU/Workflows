# -*- coding: utf-8 -*-

import numpy as np
import itertools
#lee un txt llamado doe_seed.txt que contiene una linea por cada
#variable, en cada linea aparecen el minimo y maximo valor
#y un 0 para variables lineales, 1 para logaritmicas

def sampling(input_file):
    casos =[]
    with open(input_file, 'r') as f:
        fflvl = int(f.readline())
        for row in f:
            casos.append(row.split())
    casos = np.asarray(casos, dtype = float)
    X = np.zeros((len(casos), fflvl),float)
    ii = 0
    for entrada in casos:
        if entrada[2] == 0:
            X[ii] = np.linspace(entrada[0], entrada[1], fflvl)
        elif entrada[2] == 1:
            X[ii] = np.geomspace(entrada[0], entrada[1], fflvl)
        ii+=1

    number=1
    i=0
    X_fact=np.zeros((int(fflvl**len(casos)),len(casos)),float)
    args = ()
    for ii in range(len(casos)):
        b = (X[ii,:])
        args += (b,)
    for combination in itertools.product(*args):
        X_fact[i,:] = (combination)
        i +=1
        number+=1
    return X_fact
    #np.savetxt('doe_file.txt', X_fact, ['%i','%i','%i','%i','%.4e'], delimiter = '\t')