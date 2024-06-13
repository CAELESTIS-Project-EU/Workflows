# -*- coding: utf-8 -*-

import numpy as np
import shutil
import os
import time
from pycompss.api.task import task
from pycompss.api.constraint import constraint
from pycompss.api.parameter import *

from PHASES.MESHER.permeability_mesher.WriteAlyaBou import writeAlyaBou
from PHASES.MESHER.permeability_mesher.WriteAlyaFix import writeAlyaFix
from PHASES.MESHER.permeability_mesher.WriteAlyaFie import writeAlyaFie
from PHASES.MESHER.permeability_mesher.WriteAlyaSet import writeAlyaSet
from PHASES.MESHER.permeability_mesher.WriteAlyaSet6 import writeAlyaSet6
from PHASES.MESHER.permeability_mesher.WriteAlyaMat import writeAlyaMat
from PHASES.MESHER.permeability_mesher.WriteAlyaNsi import writeAlyaNsi
from PHASES.MESHER.permeability_mesher.WriteAlyaDom import writeAlyaDom
from PHASES.MESHER.permeability_mesher.WriteAlyaDat import writeAlyaDat
from PHASES.MESHER.permeability_mesher.WriteAlyaKer import writeAlyaKer
from PHASES.MESHER.permeability_mesher.WriteAlyaPos import writeAlyaPos
from PHASES.MESHER.permeability_mesher.WriteJobLauncher import writeJobLauncher
from PHASES.MESHER.permeability_mesher.WriteAlyaGeo import writeAlyaGeo

from PHASES.MESHER.permeability_mesher.GenGeometry import generar_superficies_rectangulares
from PHASES.MESHER.permeability_mesher.GenGeometry import generar_superficies_puntos
from PHASES.MESHER.permeability_mesher.GenCases import NoFallos
from PHASES.MESHER.permeability_mesher.GenCases import Overlap
from PHASES.MESHER.permeability_mesher.GenCases import Gap
from PHASES.MESHER.permeability_mesher.FVF_variation_defects import FVF_variation
from PHASES.MESHER.permeability_mesher.GenerateMeshOris import Mesh_and_Oris

def permeability_from_doe(**kwargs):
    values=kwargs.get("values")
    kwargs['density'] = values['Density']
    kwargs['viscosity'] = values['Viscosity']
    kwargs['gravity'] = values['Gravity']
    kwargs['volume_fraction'] = values['FVF_component']
    kwargs['w_tow'] = values['w_tow']
    kwargs['h_tow'] = values['h_tow']
    kwargs['L_pro'] = values['L_pro']
    kwargs['n_tows'] = values['n_tows']
    kwargs['tipo_fallo'] = values['Defect']
    kwargs['consider_FVF_variation'] = values['FVF_variation']
    kwargs['Full_periodicity'] = values['Full_Periodicity']
    kwargs['n_elementos_gap'] = values['n_elements_gap']
    kwargs['n_elementos_capa'] = values['n_elements_layer']
    kwargs['n_elementos_towsingap'] = 100
    kwargs['angulos_tows'] = [values['angle_1'], values['angle_2'], values['angle_3'], values['angle_4'],
                              values['angle_5'], values['angle_6']]
    kwargs['n_capas'] = len(kwargs['angulos_tows'])
    kwargs['Lset'] = values['Lset']
    kwargs['ol'] = values['Defect_Size']
    kwargs['ol_izd'] = values['Defect_Transition']
    kwargs['ol_drch'] = values['Defect_Transition']
    kwargs['factor_desplazamiento'] = 1 / 10
    kwargs['ajus_ol'] = 5 / 6
    kwargs['AlyaSet'] = 'Feat'  # or 'All' as needed
    kwargs['debug'] = False
    kwargs['debugELSET'] = False

    del kwargs['values']
    return RVEgen2Alya(**kwargs)

def permeability_mesher(**kwargs):
    for item in kwargs['problem_mesher']:
        kwargs.update(item)
    values=kwargs.get("values")
    kwargs['angles_tows'] = [values['angle_1'], values['angle_2'], values['angle_3'], values['angle_4'], values['angle_5'], values['angle_6']]

    del kwargs['problem_mesher']
    return RVEgen2Alya(**kwargs)


@constraint(computing_units='$RVEGEN_CUS')
@task(returns=1)
def RVEgen2Alya(simulation_wdir, case_name, density, viscosity, gravity, volume_fraction, tipo_fallo, factor_desplazamiento, w_tow,
                h_tow, L_pro, n_elementos_gap, n_elementos_towsingap,
                n_elementos_capa, n_capas, angulos_tows, n_tows, Lset, ol, ajus_ol, ol_izd, ol_drch, AlyaSet, debug, consider_FVF_variation, Full_periodicity, **kwargs):
    outputPath = f'{simulation_wdir}'
    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)
    print(f'Case_name = {case_name}')
    outputMeshPath = f'{simulation_wdir}/msh/'
    if not os.path.isdir(outputMeshPath):
        os.makedirs(outputMeshPath)


    print("    Generating geometry ...")

    # Get the start time
    st = time.time()

    # --------------------------------------------
    #
    # Units
    #
    #   Variable  Description              SI (m)  SI (mm)
    #       nu    Viscosity                 Pa·s      MPa·s
    #       Kxx   Permeability in long.     m^2       mm^2
    #       Kyy   Permeability in tran.     m^2       mm^2
    #       P     Pressure                  Pa        MPa
    #       rho   Density                   kg/m^3    tonne/mm^3
    #       v     Velocity                  m/s       mm/s
    #
    # --------------------------------------------

    # --------------------------------------------
    #
    # Inputs
    # UNITS: SI
    # --------------------------------------------

    # Problem setup
    TotalTimeSimulation = 1000.0
    MaxNumSteps = 1e6
    periodicityMethod = 'Automatic'
    fieldFlag = True

    simulaciones = ["x-flow", "y-flow", "z-flow"]

    # %%
    # --------------------------------------------
    #
    # Crear la geometria y malla
    #
    # --------------------------------------------

    inicio = time.time()
    ###################################################################
    ###################################################################
    ###################################################################

    if tipo_fallo == "N":
        datos_input, n_nodos, n_espesor, Ldom, desfase_array, mov_geometria_array = NoFallos(w_tow, h_tow, L_pro,
                                                                                             angulos_tows, n_capas,
                                                                                             n_tows, n_elementos_gap,
                                                                                             n_elementos_towsingap,
                                                                                             n_elementos_capa,
                                                                                             factor_desplazamiento)
    elif tipo_fallo == "O":
        datos_input, n_nodos, n_espesor, Ldom, desfase_array, mov_geometria_array = Overlap(w_tow, h_tow, L_pro, ol,
                                                                                            ajus_ol, ol_izd, ol_drch,
                                                                                            angulos_tows, n_capas,
                                                                                            n_tows, n_elementos_gap,
                                                                                            n_elementos_towsingap,
                                                                                            n_elementos_capa,
                                                                                            factor_desplazamiento)
    elif tipo_fallo == "G":
        datos_input, n_nodos, n_espesor, Ldom, desfase_array, mov_geometria_array = Gap(w_tow, h_tow, L_pro, ol,
                                                                                        ajus_ol, ol_izd, ol_drch,
                                                                                        angulos_tows, n_capas, n_tows,
                                                                                        n_elementos_gap,
                                                                                        n_elementos_towsingap,
                                                                                        n_elementos_capa,
                                                                                        factor_desplazamiento)


    combined = []
    planos_Yarn = []
    centros_Yarn = []
    contarTow = 0
    for i in datos_input:
        contarTow += 1
        if int((len(i[0]) - 3) / 3) == 1:
            comb, plan, cent = generar_superficies_rectangulares(i)
        else:
            comb, plan, cent = generar_superficies_puntos(i)
        combined.append(comb)
        planos_Yarn.append(plan)
        centros_Yarn.append(cent)

        # Ruta del archivo de salida STL
        archivo_stl = outputPath + '/' + 'tow_{}.stl'.format(contarTow)

        # Guardar el objeto STL en un archivo
        combined[contarTow - 1].save(archivo_stl)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Geometry generation time: {round(tiempo_ej / 60, 2)} min")

    print(f"    The model will have {(n_nodos - 1) * (n_nodos - 1) * (n_espesor - 1)} elements")

    ##########################################
    ##########################################

    # %%

    # Mesh and orientation

    inicio = time.time()

    dimXc, dimYc, dimZc, matriz_4d, matriz_4dc, matriz_3dc_inout, matriz_3dc_oris, nodes = Mesh_and_Oris(Ldom, n_nodos,
                                                                                                         n_capas, h_tow,
                                                                                                         n_espesor,
                                                                                                         datos_input,
                                                                                                         outputPath,
                                                                                                         planos_Yarn,
                                                                                                         centros_Yarn)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Mesh and Oris generation time: {round(tiempo_ej / 60, 2)} min")

    # %%

    # --------------------------------------------
    #
    # Alya files
    #
    # --------------------------------------------

    inicio = time.time()
    print('    Calculating FVF_tows ...')

    # Creamos una copia de la matriz que tiene la información de a qué tow pertenece cada elemento
    matriz_3dc_FVF = matriz_3dc_inout.astype(float)
    # Cálculo teórico del FVF de los tows para tener un FVF de componente dado
    volume_fraction_tows = (volume_fraction * (w_tow + L_pro)) / w_tow
    # Los elementos que pertenecen a tow los ponemos con FVF
    matriz_3dc_FVF[matriz_3dc_FVF != 0] = volume_fraction_tows
    # Busca si hay overlap para cambiar la FVF
    if tipo_fallo == 'O' or tipo_fallo == 'G':
        if consider_FVF_variation == True:
            matriz_3dc_FVF = FVF_variation(matriz_3dc_inout, n_capas, matriz_3dc_FVF, ajus_ol)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        FVF generation time: {round(tiempo_ej / 60, 2)} min")

    # --------------------------------------------

    inicio = time.time()
    print('    Writting Alya files ...')
    print('    Writting Alya jobName.geo.dat ...')

    # Alya geo file
    Elementsetmaterials, numero_elemento, posicion_n_nodo, Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array = writeAlyaGeo(
        outputMeshPath, case_name, dimXc, dimYc, dimZc, matriz_4d, matriz_4dc, matriz_3dc_inout, matriz_3dc_oris,
        angulos_tows, n_elementos_capa, matriz_3dc_FVF)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Geo file generation time: {round(tiempo_ej / 60, 2)} min")

    # --------------------------------------------
    #
    # Alya .mat.dat
    # The number of materials is harcoded to be always 2: fibre and matrix
    # --------------------------------------------
    inicio = time.time()
    print('    Writting Alya jobName.mat.dat ...')
    nmate = writeAlyaMat(outputMeshPath, case_name, Elementsetmaterials)
    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Mat file generation time: {round(tiempo_ej / 60, 2)} min")
    # --------------------------------------------
    #
    # Alya .bou.dat and .fix.dat
    #
    # --------------------------------------------
    inicio = time.time()

    print('    Writting Alya jobName.bou.dat ...')

    nboun = 0
    b_list1 = []
    for j in range(len(numero_elemento[0, :, 0])):
        for k in range(len(numero_elemento[0, 0, :])):
            b_list1.append([int(posicion_n_nodo[0, j, k]), int(posicion_n_nodo[0, j, k + 1]),
                            int(posicion_n_nodo[0, j + 1, k + 1]), int(posicion_n_nodo[0, j + 1, k]),
                            int(numero_elemento[0, j, k])])
            nboun += 1
    b_list2 = []
    for j in range(len(numero_elemento[-1, :, 0])):
        for k in range(len(numero_elemento[-1, 0, :])):
            b_list2.append([int(posicion_n_nodo[-1, j, k]), int(posicion_n_nodo[-1, j + 1, k]),
                            int(posicion_n_nodo[-1, j + 1, k + 1]), int(posicion_n_nodo[-1, j, k + 1]),
                            int(numero_elemento[-1, j, k])])
            nboun += 1
    b_list3 = []
    for i in range(len(numero_elemento[:, 0, 0])):
        for k in range(len(numero_elemento[0, 0, :])):
            b_list3.append([int(posicion_n_nodo[i, 0, k]), int(posicion_n_nodo[i + 1, 0, k]),
                            int(posicion_n_nodo[i + 1, 0, k + 1]), int(posicion_n_nodo[i, 0, k + 1]),
                            int(numero_elemento[i, 0, k])])
            nboun += 1
    b_list4 = []
    for i in range(len(numero_elemento[:, -1, 0])):
        for k in range(len(numero_elemento[-1, 0, :])):
            b_list4.append(
                [int(posicion_n_nodo[i + 1, -1, k]), int(posicion_n_nodo[i, -1, k]), int(posicion_n_nodo[i, -1, k + 1]),
                 int(posicion_n_nodo[i + 1, -1, k + 1]), int(numero_elemento[i, -1, k])])
            nboun += 1
    b_list5 = []
    for i in range(len(numero_elemento[:, 0, 0])):
        for j in range(len(numero_elemento[0, :, 0])):
            b_list5.append([int(posicion_n_nodo[i, j + 1, 0]), int(posicion_n_nodo[i + 1, j + 1, 0]),
                            int(posicion_n_nodo[i + 1, j, 0]), int(posicion_n_nodo[i, j, 0]),
                            int(numero_elemento[i, j, 0])])
            nboun += 1
    b_list6 = []
    for i in range(len(numero_elemento[:, -1, 0])):
        for j in range(len(numero_elemento[-1, :, 0])):
            b_list6.append([int(posicion_n_nodo[i, j, -1]), int(posicion_n_nodo[i + 1, j, -1]),
                            int(posicion_n_nodo[i + 1, j + 1, -1]), int(posicion_n_nodo[i, j + 1, -1]),
                            int(numero_elemento[i, j, -1])])
            nboun += 1

    b_list = [b_list1, b_list2, b_list3, b_list4, b_list5, b_list6]

    writeAlyaBou(outputMeshPath, case_name, b_list)
    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Bou file generation time: {round(tiempo_ej / 60, 2)} min")
    inicio = time.time()

    print('    Writting Alya jobName.fix.dat ...')
    writeAlyaFix(outputMeshPath, case_name, b_list)

    numerodenodos = int(len(posicion_n_nodo[:, 0, 0]) * len(posicion_n_nodo[0, :, 0]) * len(posicion_n_nodo[0, 0, :]))
    numerodeelementos = len(Elementsetmaterials[:, 0])
    numerodeboundelems = nboun

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Fix file generation time: {round(tiempo_ej / 60, 2)} min")
    # --------------------------------------------
    #
    # Alya .fie.dat (porosity tensor)
    #
    # --------------------------------------------
    inicio = time.time()

    print('    Writting Alya jobName.fie.dat ...')

    writeAlyaFie(outputMeshPath, case_name, viscosity, Elementsetmaterials, numerodeelementos, Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Fie file generation time: {round(tiempo_ej / 60, 2)} min")

    # --------------------------------------------
    #
    # Alya Set
    #
    # --------------------------------------------

    inicio = time.time()

    print('    Writting Alya jobName.set.dat ...')

    # Alya Set
    if AlyaSet == 'All':
        writeAlyaSet(outputMeshPath, case_name, numerodeelementos, numerodeboundelems)
    else:
        writeAlyaSet6(outputMeshPath, case_name, Lset, n_capas, nodes, L_pro, Ldom, volume_fraction, ol, ol_izd, ol_drch,
                      angulos_tows, w_tow, tipo_fallo, matriz_3dc_FVF, datos_input, matriz_4dc)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Set file generation time: {round(tiempo_ej / 60, 2)} min")

    # --------------------------------------------
    #
    # Alya periodicity file (NOT NEEDED)
    #
    # --------------------------------------------

    ### ESTA PARTE HABRÍA QUE REVISARLA PARA USARLA

    if periodicityMethod == 'Manual':
        print('NOT MANTAINED!!!!!!')
    else:
        print('    NOTE: Periodicity is imposed automatically by Alya ...')

    # --------------------------------------------
    #
    # End generating Alya mesh files
    #
    # --------------------------------------------

    # --------------------------------------------
    #
    # Alya configuration files for each flow direction
    #
    # --------------------------------------------
    inicio = time.time()

    print('    Writting Alya Configuration files ...')

    lx = Ldom  # Esto son mm
    ly = Ldom  # Esto son mm
    lz = n_capas * h_tow  # Esto son mm
    length = [lx * 1e-3, ly * 1e-3, lz * 1e-3]  # Aquí se pasa a metros. Unidades ALYA metros
    for j in range(len(simulaciones)):
        path = outputPath + '/' + str(simulaciones[j]) + '/'
        os.makedirs(path)
        fileName = case_name
        icase = str(simulaciones[j])

        node = 1  # TODO: Coger un nodo que no este en la direccion del flow (solo en z)
        # Preliminary calculations
        #		gravity = Presion_de_inyeccion/(density*length[j])
        Presion_de_inyeccion = gravity * (density * length[j])

        # Alya Dom
        writeAlyaDom(path, fileName, icase, int(numerodenodos), numerodeelementos, numerodeboundelems, nmate,
                     periodicityMethod, fieldFlag, Full_periodicity)
        # Alya Dat
        writeAlyaDat(debug, path, fileName, TotalTimeSimulation, MaxNumSteps)
        # Alya Ker
        writeAlyaKer(debug, path, fileName, nmate, density, viscosity)
        # Alya Nsi
        writeAlyaNsi(debug, path, fileName, icase, Presion_de_inyeccion, gravity, lx, ly, lz, node, Full_periodicity)
        # Alya Pos
        writeAlyaPos(path, fileName)

        # Job Launcher
        #writeJobLauncher(path, fileName, queue, numCPUs)

    # Get the end time
    et = time.time()

    # Get the execution time
    elapsed_time = et - st

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Configuration files generation time: {round(tiempo_ej / 60, 2)} min")
    print('  Total execution time:', round(elapsed_time / 60, 2), 'min')

    return