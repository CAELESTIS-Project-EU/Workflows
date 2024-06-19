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
import os
from PHASES.MESHER.permeability_mesher.PermeabilityCalc import Permeability_Calculation_sim
from PHASES.MESHER.permeability_mesher.WriteAlyaSet4 import AdjSets

# leemos que es cada columna al principio
# nos quedamos la ultima iteracion


def postProcessPermeability(**kwargs):
    values = kwargs.get("values")
    kwargs['w_tow'] = values['w_tow']
    kwargs['L_pro'] = values['L_pro']
    kwargs['angulos_tows'] = [values['angle_1'], values['angle_2'], values['angle_3'], values['angle_4'],
                              values['angle_5'], values['angle_6']]
    kwargs['n_tows'] = values['n_tows']
    kwargs['Lset'] = values['Lset']
    kwargs['gravity'] = values['Gravity']
    kwargs['density'] = values['Density']
    kwargs['viscosity'] = values['Viscosity']
    kwargs['n_capas'] = len(kwargs['angulos_tows'])
    kwargs['n_elementos_gap']= values['n_elements_gap']
    kwargs['n_elementos_towsingap'] = 100
    del kwargs['values']
    return postproCaso(**kwargs)



@on_failure(management='IGNORE')
@task(out=COLLECTION_IN, returns=1)
def postproCaso(simulation_wdir, case_name, w_tow, L_pro, angulos_tows, n_tows, n_capas, Lset, gravity, density, viscosity, n_elementos_gap, n_elementos_towsingap, out, **kwargs):
    num_caso=extract_number(case_name)
    archivo_x = 'x-flow/'+ case_name+ '-element.nsi.set'
    archivo_y = 'y-flow/'+ case_name+ '-element.nsi.set'
    archivo_z = 'z-flow/'+ case_name+ '-element.nsi.set'

    archivos = [archivo_x, archivo_y, archivo_z]
    for angulo in angulos_tows:
        if angulo == 0 or angulo == 90:
            angulo_dist_0_90 = 90.0
        else:
            angulo_dist_0_90 = angulo
            break
    Ldom = n_tows * (w_tow + L_pro) / math.sin(math.radians(angulo_dist_0_90))
    seed_XY = L_pro / n_elementos_gap
    if L_pro == 0:
        seed_XY = w_tow / n_elementos_towsingap
    n_nodos = round(Ldom / seed_XY + 1)
    nodos = n_nodos - 1
    EpS = int(np.ceil(Lset / (L_pro / n_elementos_gap)))
    LsetReal = EpS * (Ldom / nodos)
    dimZc = n_capas
    nOut = 6

    for n, direccion in enumerate(archivos):
        header = []
        last_iter_R = []
        last_iter = []
        with open(os.path.join(simulation_wdir, direccion), 'r') as f:
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
        if n == 0:
            sets = np.zeros([len(last_iter), 1 + nOut * 3])
            sets[:, 0] = np.asarray(last_iter, dtype=float)[:, 0]
        sets[:, 1 + n * nOut:1 + (n + 1) * nOut] = np.asarray(last_iter, dtype=float)[:, 2:]
    extrasets = []
    iset = 1
    dimXc = math.sqrt(len(last_iter) / dimZc)
    dimYc = dimXc
    nsetscapa = dimXc * dimYc
    for order in range(5):
        for set1 in sets:
            if (order <= ((set1[0] - 1) % nsetscapa) % dimXc < (dimXc - order)) and (
                    order <= int(((set1[0] - 1) % nsetscapa) / dimYc) < (dimXc - order)):
                neighbours = AdjSets(set1[0] - 1, dimXc, order)
                setstomerge = sets[neighbours.astype(int)]
                setstomerge[:, 0] = iset
                extrasets.append(np.r_[num_caso, iset, LsetReal * (order * 2 + 1), np.mean(setstomerge, axis=0)[1:]])
                iset += 1
    extrasets = np.asarray(extrasets)

    np.savetxt(os.path.join(simulation_wdir,'set_results.csv'), extrasets, delimiter=',')
    ruta_caso = simulation_wdir
    ruta_mesh = os.path.join(ruta_caso, 'msh')
    set_outputs = np.loadtxt(os.path.join(ruta_caso, 'set_results.csv'), delimiter=',')
    for file in os.listdir(ruta_mesh):
        if '.txt' in file and os.stat(os.path.join(ruta_mesh, file)).st_size != 0:
            set_results = []
            toRom = []
            set_inputs = []
            with open(os.path.join(ruta_mesh, file), 'r') as f:
                for line in f:
                    new_line = line.replace(',', ' ')
                    splitline = re.split('\s+', new_line)[:-1]
                    set_inputs.append(splitline)
            set_inputs = np.asarray(set_inputs, dtype=float)
            set_output_dict = {tuple(row[:2]): row[3:] for row in set_outputs}
            for line_in in set_inputs:
                key = tuple(line_in[:2])
                if key in set_output_dict:
                    line_out = set_output_dict[key]
                    set_results.append(np.r_[line_in, line_out])
            set_results = np.asarray(set_results)
            for line in set_results:
                evl, evt0, evt1, Permeability_tensor = Permeability_Calculation_sim(gravity, density, viscosity,
                                                                                    line[-18:])
                toRom.append(np.r_[line[:-18], evl, evt0, evt1, Permeability_tensor])
            np.savetxt(os.path.join(ruta_caso, 'toRom' + file), np.asarray(toRom))
    return np.asarray(toRom)


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


@on_failure(management='IGNORE')
@task(out=COLLECTION_IN, returns=1)
def JoinCases(simulation_wdir, results_folder, out, erase_previous = True, **kwargs):
    name_files = ['toRomallsets.csv']
    debug_headers = 'case;set;Lset;x;y;z;layer;h_tow;FVF_tow;FVF_set;llori;ilori;ulori;'
    gap_headers = 'gap;dgap;sgap;'
    ol_headers1 = 'ol;'
    ol_headers2 = 'dol;sol;adjgap;dadjgap;sadjgap;'
    out_headers = 'k1;k2;k3;pv1x;pv1y;pv1z;pv2x;pv2y;pv2z;Perm_xx;Perm_xy;Perm_xz;Perm_yy;Perm_yz;Perm_zz'
    for geom in name_files:
        content = []
        for caso in os.listdir(simulation_wdir):
            if geom.replace('csv', 'txt') in os.listdir(os.path.join(simulation_wdir, str(caso))):
                file = os.path.join(simulation_wdir, str(caso), geom.replace('csv', 'txt'))
                with open(file, 'r') as f:
                    for line in f:
                        content.append(line.split(' '))
        all_cases = np.asarray(content,dtype = float)
        n_capas = 6
        oris = np.zeros([len(all_cases),3])
        for i, sets in enumerate(all_cases):
            oris[i,1] = sets[10+int((sets[6])%n_capas)]
            oris[i,0] = sets[10+int((sets[6]-1)%n_capas)]
            oris[i,2] = sets[10+int((sets[6]+1)%n_capas)]

        todebug = np.c_[all_cases[:,:10],oris,all_cases[:,10+n_capas+7:]]
        file_out2 = geom.replace('toRom', 'RawResults')
        np.savetxt(os.path.join(results_folder,file_out2),todebug, delimiter = ';', header=debug_headers+gap_headers+ol_headers1+ol_headers2+out_headers, comments='')
    return