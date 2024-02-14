# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 09:25:05 2023

Itera por los casos calculados para unir los resultados y poder introducirlos a Twinkle

@author: rteruel
"""
# import numpy as np
import os
# import pandas as pd

def JoinCases(casos_path, outfile, erase_previous = True):
    if erase_previous:
        open(outfile, 'w').close()
    # casos_path = 'output/'
    lista_casos = os.listdir(casos_path)
    s1 = 'variable1s1;variable2s1;variable3s1;variable4s1;variable5s1;'
    s2 = 'variable1s2;variable2s2;variable3s2;variable4s2;variable5s2;'
    s3 = 'variable1s3;variable2s3;variable3s3;variable4s3;variable5s3'
    with open(outfile, 'a') as f:
        f.write('simulacion;set;' + s1 + s2 + s3 + '\n')
    for caso in lista_casos:
        with open(casos_path + caso + '/set_results.csv', 'r') as f:
            new_case = f.readlines()
            # Reemplazar comas por punto y coma (;) en cada línea
            modified_lines = [line.replace(',', ';') for line in new_case]

        with open(outfile, 'a') as f:
            f.writelines(modified_lines)
        