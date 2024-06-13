
import numpy as np
import math
from src.WriteAlyaSet6 import AdjSets
import os
import re
from src.PermeabilityCalc import Permeability_Calculation_sim
#leemos que es cada columna al principio
#nos quedamos la ultima iteracion

def postproCaso(num_caso, w_tow, L_pro, angulos_tows, n_tows, n_capas, Lset, gravity, density, viscosity, n_elementos_gap, n_elementos_towsingap):
    path_caso = 'output/Caso_' + str(num_caso) + '/'
    archivo_x = 'x-flow/Caso_'+str(num_caso)+'-element.nsi.set'
    archivo_y = 'y-flow/Caso_'+str(num_caso)+'-element.nsi.set'
    archivo_z = 'z-flow/Caso_'+str(num_caso)+'-element.nsi.set'
    archivos = [archivo_x,archivo_y,archivo_z]
    for angulo in angulos_tows:
        if angulo==0 or angulo==90:
            angulo_dist_0_90 = 90.0
        else:
            angulo_dist_0_90 = angulo
            break
    Ldom = n_tows*(w_tow+L_pro)/math.sin(math.radians(angulo_dist_0_90))
    seed_XY = L_pro/n_elementos_gap
    if L_pro==0:
        seed_XY = w_tow/n_elementos_towsingap
    n_nodos = round(Ldom/seed_XY +1)
    nodos = n_nodos-1
    EpS = int(np.ceil(Lset/(L_pro/n_elementos_gap)))
    LsetReal = EpS*(Ldom/nodos)
    dimZc = n_capas  
    nOut = 6
    
    for n, direccion in enumerate(archivos):
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
        if n==0:
            sets = np.zeros([len(last_iter), 1+nOut*3])
            sets[:,0] = np.asarray(last_iter, dtype = float)[:,0]
        sets[:,1+n*nOut:1+(n+1)*nOut] = np.asarray(last_iter, dtype = float)[:,2:]
    extrasets = []
    iset = 1
    dimXc = math.sqrt(len(last_iter)/dimZc)
    dimYc = dimXc
    nsetscapa = dimXc*dimYc
    for order in range(5):
        for set1 in sets:
            if  (order <= ((set1[0]-1)%nsetscapa)%dimXc < (dimXc - order)) and (order <= int(((set1[0]-1)%nsetscapa)/dimYc) < (dimXc-order)):
                neighbours = AdjSets(set1[0]-1,dimXc,order)
                setstomerge = sets[neighbours.astype(int)]
                setstomerge[:,0] = iset
                extrasets.append(np.r_[num_caso, iset, LsetReal*(order*2+1), np.mean(setstomerge,axis = 0)[1:]])
                iset += 1
    extrasets = np.asarray(extrasets)

    np.savetxt(path_caso+'set_results.csv', extrasets, delimiter = ',')    
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
            set_output_dict = {tuple(row[:2]): row[3:] for row in set_outputs}
            for line_in in set_inputs:
                key = tuple(line_in[:2])
                if key in set_output_dict:
                    line_out = set_output_dict[key]
                    set_results.append(np.r_[line_in, line_out])
            set_results = np.asarray(set_results)
            for line in set_results:
                evl, evt0, evt1, Permeability_tensor = Permeability_Calculation_sim(gravity, density, viscosity, line[-18:])
                toRom.append(np.r_[line[:-18],evl,evt0,evt1,Permeability_tensor])
            np.savetxt(os.path.join(ruta_caso,'toRom'+file),np.asarray(toRom))

    
    return