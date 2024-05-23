# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 12:58:51 2023

@author: rteruel
"""

import numpy as np
import math
from PHASES.MESHER.permeability_mesher.WriteAlyaSet4 import AdjSets
import os
import re
from PHASES.MESHER.permeability_mesher.PermeabilityCalc import Permeability_Calculation_sim
#leemos que es cada columna al principio
#nos quedamos la ultima iteracion

@task(out=COLLECTION_IN, returns=1)
def postproCaso(case_name, w_tow, L_pro, angulos_tows, n_tows, n_capas, Lset, gravity, density, viscosity,  **kwargs):
    path_caso = 'output/'+case_name+'/'
    archivo_x = 'x-flow/Caso_'+str(num_caso)+'-element.nsi.set'
    archivo_y = 'y-flow/Caso_'+str(num_caso)+'-element.nsi.set'
    archivo_z = 'z-flow/Caso_'+str(num_caso)+'-element.nsi.set'
    archivos = [archivo_x,archivo_y,archivo_z]
    for angulo in angulos_tows:
        if angulo==0 or angulo==90:
            angulo_dist_0_90 = 90.0
        else:
            angulo_dist_0_90 = angulo
    Ldom = n_tows*(w_tow+L_pro)/math.sin(math.radians(angulo_dist_0_90))
    dimYc = int(Ldom/Lset)
    dimXc = int(Ldom/Lset)
    nsetscapa = dimXc*dimYc
    dimZc = n_capas  
    nOut = 6
    # joint_sets = np.zeros([len(archivos), dimXc-2, dimYc-2, dimZc, nOut])

    sets = np.zeros([dimXc*dimYc*dimZc, 1+nOut*3])
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
        sets[:,1+n*nOut:1+(n+1)*nOut] = np.asarray(last_iter, dtype = float)[:,2:]
        sets[:,0] = np.asarray(last_iter, dtype = float)[:,0]
    extrasets = []
    iset = 1
    for order in range(3):
        for set1 in sets:
            if  (order <= (set1[0]%nsetscapa)%dimXc < (dimXc - order)) and (order <= int((set1[0]%nsetscapa)/dimYc) < (dimXc-order)):
                neighbours = AdjSets(set1[0]-1,dimXc,order)
                setstomerge = sets[neighbours.astype(int)]
                setstomerge[:,0] = iset
                extrasets.append(np.r_[num_caso, iset, Lset*(order*2+1), np.mean(setstomerge,axis = 0)[1:]])
                iset += 1
    extrasets = np.asarray(extrasets)

    np.savetxt(path_caso+'set_results.csv', extrasets, delimiter = ',')    
    # setfiles = os.listdir('output/Caso_'+str(num_caso)+'/msh')
    ruta_caso = 'output/Caso_'+str(num_caso)
    ruta_mesh = os.path.join(ruta_caso,'msh')
    set_outputs = np.loadtxt(os.path.join(ruta_caso,'set_results.csv'),delimiter = ',')
    for file in os.listdir(ruta_mesh):
        if '.txt' in file and os.stat(os.path.join(ruta_mesh,file)).st_size != 0:
            set_results = []
            toRom = []
            set_inputs = []
            with open(os.path.join(ruta_mesh,file), 'r') as f:
                for line in f:
                    new_line = line.replace(',',' ')
                    splitline = re.split('\s+', new_line)[:-1]
                    set_inputs.append(splitline)
            set_inputs =np.asarray(set_inputs, dtype = float)
            for line_in in set_inputs:
                line_out = set_outputs[np.all(set_outputs[:,:3] == line_in[:3], axis=1), 3:]
                if len(line_out) != 0:
                    set_results.append(np.r_[line_in, line_out[0]])
            set_results = np.asarray(set_results)
            for line in set_results:
                evl, evt0, evt1 = Permeability_Calculation_sim(gravity, density, viscosity, line[-18:])
                toRom.append(np.r_[line[:-18],evl,evt0,evt1])
            np.savetxt(os.path.join(ruta_caso,'toRom'+file),np.asarray(toRom))
    return