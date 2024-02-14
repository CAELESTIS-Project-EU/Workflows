# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 12:58:51 2023

@author: rteruel
"""

import numpy as np
import math
#leemos que es cada columna al principio
#nos quedamos la ultima iteracion
def postproCaso(NumCaso, anchura, Lpro, angulos_tows, n_tows, n_capas, Lset):
    path_caso = 'output/Caso_' + str(NumCaso) + '/'
    archivo_x = 'x-flow/Caso_'+str(NumCaso)+'-element.nsi.set'
    archivo_y = 'y-flow/Caso_'+str(NumCaso)+'-element.nsi.set'
    archivo_z = 'z-flow/Caso_'+str(NumCaso)+'-element.nsi.set'
    archivos = [archivo_x,archivo_y,archivo_z]
    for angulo in angulos_tows:
        if angulo==0 or angulo==90:
            angulo_dist_0_90 = 90.0
        else:
            angulo_dist_0_90 = angulo
    Ldom = n_tows*(anchura+Lpro)/math.sin(math.radians(angulo_dist_0_90))
    dimYc = math.ceil(Ldom/Lset)
    dimXc = math.ceil(Ldom/Lset)
    dimZc = n_capas  
    nOut = 6
    joint_sets = np.zeros([len(archivos), dimXc-2, dimYc-2, dimZc, nOut])
    for n, direccion in enumerate(archivos):
        # direccion = 'x-element.nsi.set'
        header = []
        last_iter_R = []
        last_iter = []
        with open(path_caso + direccion, 'r') as f:
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
        sets = np.asarray(last_iter, dtype = float)
        # sets = sets[:,1:]
        sets4d = np.reshape(sets, [dimXc, dimYc, dimZc, nOut])
        iset = 0
        for x in range(1,dimXc-1):
            for y in range(1,dimYc-1):
                for z in range(dimZc):
                    joint_sets[n,x-1,y-1,z] = np.r_[iset,np.mean(np.c_[sets4d[x-1,y-1,z,1:], sets4d[x-1,y,z,1:], sets4d[x,y+1,z,1:],
                                                    sets4d[x,y-1,z,1:], sets4d[x,y,z,1:], sets4d[x,y+1,z,1:],
                                                    sets4d[x+1,y-1,z,1:], sets4d[x+1,y,z,1:], sets4d[x,y+1,z,1:]], axis = 1)]
                    iset += 1
    nsets2 = (dimXc-2)*(dimYc-2)*dimZc
    ujsets = np.c_[NumCaso*np.ones(nsets2), np.reshape(joint_sets[0], [nsets2,6]),
                   np.reshape(joint_sets[0], [nsets2,6])[:,1:],np.reshape(joint_sets[0], [nsets2,6])[:,1:]]
    np.savetxt(path_caso+'set_results.csv', ujsets, delimiter = ',')