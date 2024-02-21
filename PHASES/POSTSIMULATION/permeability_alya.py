# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 12:58:51 2023

@author: rteruel
"""
import os
import re
from pycompss.api.task import task
from pycompss.api.parameter import *
import numpy as np
import math


# leemos que es cada columna al principio
# nos quedamos la ultima iteracion


def postProcessPermeability(**kwargs):
    for item in kwargs['postProcessParam']:
        kwargs.update(item)
    values = kwargs.get("values")
    kwargs['angles_tows'] = [values[0], values[1], values[2], values[3]]
    kwargs['L_pro'] = values[4]
    del kwargs['postProcessParam']
    return postproCaso(**kwargs)



@task(out=COLLECTION_IN, returns=1)
def postproCaso(simulation_wdir, case_name, w_tow, L_pro, angles_tows, n_tows, n_layers, Lset, **kwargs):
    archivo_x = 'x-flow/' + case_name + '-element.nsi.set'
    archivo_y = 'y-flow/' + case_name + '-element.nsi.set'
    archivo_z = 'z-flow/' + case_name + '-element.nsi.set'
    num_case = int(extract_number(case_name))
    archivos = [archivo_x, archivo_y, archivo_z]
    for angulo in angles_tows:
        if angulo == 0 or angulo == 90:
            angulo_dist_0_90 = 90.0
        else:
            angulo_dist_0_90 = angulo
    Ldom = n_tows * (w_tow + L_pro) / math.sin(math.radians(angulo_dist_0_90))
    dimYc = math.ceil(Ldom / Lset)
    dimXc = math.ceil(Ldom / Lset)
    dimZc = n_layers
    nOut = 6
    joint_sets = np.zeros([len(archivos), dimXc - 2, dimYc - 2, dimZc, nOut])
    for n, direccion in enumerate(archivos):
        # direccion = 'x-element.nsi.set'
        header = []
        last_iter_R = []
        last_iter = []
        with open(simulation_wdir + "/" + direccion, 'r') as f:
            for row in f:
                if row != '# START\n':
                    header.append(row)
                else:
                    break
            content = f.readlines()
            for row in reversed(content):
                if '# Time' in row:
                    break
                last_iter_R.append(row.split())

        for row in reversed(last_iter_R):
            last_iter.append(row)
        sets = np.asarray(last_iter, dtype=float)
        # sets = sets[:,1:]
        sets4d = np.reshape(sets, [dimXc, dimYc, dimZc, nOut])
        iset = 0
        for x in range(1, dimXc - 1):
            for y in range(1, dimYc - 1):
                for z in range(dimZc):
                    joint_sets[n, x - 1, y - 1, z] = np.r_[iset, np.mean(
                        np.c_[sets4d[x - 1, y - 1, z, 1:], sets4d[x - 1, y, z, 1:], sets4d[x, y + 1, z, 1:],
                        sets4d[x, y - 1, z, 1:], sets4d[x, y, z, 1:], sets4d[x, y + 1, z, 1:],
                        sets4d[x + 1, y - 1, z, 1:], sets4d[x + 1, y, z, 1:], sets4d[x, y + 1, z, 1:]], axis=1)]
                    iset += 1
    nsets2 = (dimXc - 2) * (dimYc - 2) * dimZc
    ujsets = np.c_[num_case * np.ones(nsets2), np.reshape(joint_sets[0], [nsets2, 6]),
    np.reshape(joint_sets[0], [nsets2, 6])[:, 1:], np.reshape(joint_sets[0], [nsets2, 6])[:, 1:]]
    np.savetxt(simulation_wdir + '/set_results.csv', ujsets, delimiter=',')
    return


def extract_number(case_name):
    # Using regular expression to find the number in the string
    match = re.search(r'\d+', case_name)

    # Check if a match is found
    if match:
        # Convert the matched string to an integer and return
        return int(match.group())
    else:
        # Return None if no match is found
        return None



# import numpy as np
import os
# import pandas as pd

@task(returns=1)
def JoinCases(simulation_wdir, outputName, results_folder, erase_previous = True, **kwargs):
    outputFile= os.path.join(results_folder, outputName)
    if erase_previous:
        open(outputFile, 'w').close()
    # simulation_wdir = 'output/'
    lista_casos = os.listdir(simulation_wdir)
    s1 = 'variable1s1;variable2s1;variable3s1;variable4s1;variable5s1;'
    s2 = 'variable1s2;variable2s2;variable3s2;variable4s2;variable5s2;'
    s3 = 'variable1s3;variable2s3;variable3s3;variable4s3;variable5s3'
    with open(outputFile, 'a') as f:
        f.write('simulacion;set;' + s1 + s2 + s3 + '\n')
    for caso in lista_casos:
        with open(simulation_wdir + caso + '/set_results.csv', 'r') as f:
            new_case = f.readlines()
            # Reemplazar comas por punto y coma (;) en cada línea
            modified_lines = [line.replace(',', ';') for line in new_case]

        with open(outputFile, 'a') as f:
            f.writelines(modified_lines)
    return