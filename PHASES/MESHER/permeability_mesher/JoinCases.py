# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 09:25:05 2023

Itera por los casos calculados para unir los resultados y poder introducirlos a Twinkle

@author: rteruel
"""
# import numpy as np
import os
# import pandas as pd

def JoinCases(casos_path, outdir, erase_previous = True):
    name_files = ['toRomalltow.csv', 'toRomgap0.csv', 'toRomol0.csv',
                  'toRomol1.csv', 'toRomolM.csv', 'toRomolMgap.csv']
    common_headers = 'case,set,Lset,x,y,z,layer,fvf,plyori0,plyori1,plyori2,plyori3,plyori4,plyori5,n1,n2,n3,or01,or02,or03,dz,'
    gap_headers = 'gap,dgap,sgap,'
    ol_headers = 'ol,dol,sol,'
    out_headers = 'k1,k2,k3,pv1x,pv1y,pv1z,pv2x,pv2x,pv2z\n'
    for geom in name_files:
        
        with open(os.path.join(outdir, geom), 'a') as f:
            if geom == 'toRomalltow.csv':
                f.write(common_headers + out_headers)
            elif geom == 'toRomgap0.csv':
                f.write(common_headers + gap_headers + out_headers)
            elif geom == 'toRomolMgap.csv':
                f.write(common_headers + gap_headers + ol_headers + out_headers)
            else:
                f.write(common_headers + ol_headers + out_headers)
        
        for caso in os.listdir(casos_path):
            if geom.replace('csv', 'txt') in os.listdir(os.path.join(casos_path, str(caso))):
                file = os.path.join(casos_path, str(caso), geom.replace('csv', 'txt'))
                with open(file, 'r') as f:
                    new_case = f.readlines()  
                with open(os.path.join(outdir, geom), 'a') as f:
                    for line in new_case:   
                        f.write(line.replace(' ',','))
        
