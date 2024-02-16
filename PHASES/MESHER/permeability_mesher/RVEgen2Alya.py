# -*- coding: utf-8 -*-

import numpy as np
import shutil
import pathlib
# path = pathlib.Path(__file__).parent.resolve()
import os

path = os.getcwd()
import sys

sys.path.append(path)

import time

import math
import trimesh

from PHASES.MESHER.permeability_mesher.WriteAlyaBou import writeAlyaBou
from PHASES.MESHER.permeability_mesher.WriteAlyaFix import writeAlyaFix
from PHASES.MESHER.permeability_mesher.WriteAlyaFie import writeAlyaFie
from PHASES.MESHER.permeability_mesher.WriteAlyaSet import writeAlyaSet
from PHASES.MESHER.permeability_mesher.WriteAlyaSet2 import writeAlyaSet2
from PHASES.MESHER.permeability_mesher.WriteAlyaPer import writeAlyaPer
from PHASES.MESHER.permeability_mesher.WriteAlyaMat import writeAlyaMat

from PHASES.MESHER.permeability_mesher.WriteAlyaNsi import writeAlyaNsi
from PHASES.MESHER.permeability_mesher.WriteAlyaDom import writeAlyaDom
from PHASES.MESHER.permeability_mesher.WriteAlyaDat import writeAlyaDat
from PHASES.MESHER.permeability_mesher.WriteAlyaKer import writeAlyaKer
from PHASES.MESHER.permeability_mesher.WriteAlyaPos import writeAlyaPos
from PHASES.MESHER.permeability_mesher.WriteJobLauncher import writeJobLauncher

from PHASES.MESHER.permeability_mesher.opeAlyaRVE import getRVEnodesFromVertices
from PHASES.MESHER.permeability_mesher.opeAlyaRVE import getRVEnodesFromEdges
from PHASES.MESHER.permeability_mesher.opeAlyaRVE import addNodesFromVertices
from PHASES.MESHER.permeability_mesher.opeAlyaRVE import addNodesFromEdges
from PHASES.MESHER.permeability_mesher.opeAlyaRVE import addNodesFromFacesMeso

from PHASES.MESHER.permeability_mesher.GenGeometry import generar_superficies_rectangulares
from PHASES.MESHER.permeability_mesher.GenGeometry import generar_superficies_puntos
from PHASES.MESHER.permeability_mesher.GenCases import NoFallos
from PHASES.MESHER.permeability_mesher.GenCases import Overlap
from PHASES.MESHER.permeability_mesher.GenCases import Gap

"""def RVEgen2Alya(path, num_cases, density, viscosity, volume_fraction, tipo_fallo, w_tow, h_tow, L_pro, n_elements_gap, n_elements_towsingap,
                    n_elements_layer, n_layers, angles_tows, n_tows, Lset, ol, ajus_ol, ol_left, ol_right, AlyaSet):"""


def RVEgen2Alya(*args, **kwargs):
    for item in kwargs['problem_mesher']:
        kwargs.update(item)
    del kwargs['problem_mesher']
    # Copy updated kwargs to args
    args = kwargs.copy()

    # Remove 'problem_mesher' key from kwargs

    print("KWARGS")
    print(kwargs)
    print("ARGS")
    print(args)
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

    # Material properties
    packing = 'quad'  # 'quad' or 'hexa' packing
    if packing == 'quad':
        c = 57.0
        C1 = 16.0 / (9.0 * math.pi * math.sqrt(2.0))
        vf_max = math.pi / 4.0
    elif packing == 'hexa':
        c = 53.0
        C1 = 16.0 / (9.0 * math.pi * math.sqrt(6.0))
        vf_max = math.pi / (2.0 * math.sqrt(3.0))
    else:
        print("NO SE HA SELECCIONADO PACKING")
    R_fibra = 2.5e-6  # metros
    k_lon = (8.0 * R_fibra ** 2.0 * (1.0 - volume_fraction) ** 3.0) / (c * volume_fraction)
    k_per = C1 * R_fibra ** 2.0 * (math.sqrt(vf_max / volume_fraction) - 1.0) ** (5.0 / 2.0)
    # 	print(f"K_longitudinal = {k_lon} m2")
    # 	print(f"K_perpendicular = {k_per} m2")

    # Problem setup
    # 	debug = False
    #   Presion_de_inyeccion = 70000.0
    gravity = 10000.0
    TotalTimeSimulation = 1000.0
    MaxNumSteps = 1e6
    periodicityMethod = 'Automatic'
    fieldFlag = True

    simulaciones = ["x-flow", "y-flow", "z-flow"]

    # Nord3v2 Job setup
    # 	queue = 'debug'
    # 	numCPUs = 64

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
    ###################################################################
    # 	tipo_fallo = "O"
    # 	w_tow = 5.0
    # 	h_tow = 0.182			# Altura (espesor) de la layer.
    # 	L_pro = 0.2
    # 	n_elements_gap = 2     # Numero de elementos que queremos que haya en cada gap (colocado a 0 o 90).
    # 	# Hay que tener cuidado porque el numero de elementos del modelo crece muy rapido.
    # 	n_elements_towsingap = 100 # Numero de elementos en cada tow en caso de que L_pro=0.0
    # 	n_elements_layer = 2    # Numero de elementos que queremos que haya en cada layer
    # 	n_layers = 3	# Numero de layers que se generan
    # 	angles_tows = [0, 0, 0, 135, 0] #angles correspondiente a cada layer
    # 	n_tows = 2
    # 	Lset = 1
    # 	# Variables a continuacion seran llamadas en caso de fallo (overlap/gap)
    # 	ol = 2.0
    # 	ajus_ol = 5/6
    # 	ol_left = 0.6
    # 	ol_right = 0.6
    ###################################################################
    ###################################################################
    ###################################################################
    ###################################################################

    if tipo_fallo == "N":
        caseName = "case_" + str(num_cases)
        datos_input, n_nodos, n_espesor, Ldom = NoFallos(w_tow, h_tow, L_pro, angles_tows, n_layers, n_tows,
                                                         n_elements_gap, n_elements_towsingap, n_elements_layer)
    elif tipo_fallo == "O":
        caseName = "case_" + str(num_cases)
        datos_input, n_nodos, n_espesor, Ldom = Overlap(w_tow, h_tow, L_pro, ol, ajus_ol, ol_left, ol_right,
                                                        angles_tows, n_layers, n_tows, n_elements_gap,
                                                        n_elements_towsingap, n_elements_layer)
    elif tipo_fallo == "G":
        caseName = "Caso_" + str(num_cases)
        datos_input, n_nodos, n_espesor, Ldom = Gap(w_tow, h_tow, L_pro, ol, ajus_ol, ol_left, ol_right, angles_tows,
                                                    n_layers, n_tows, n_elements_gap, n_elements_towsingap,
                                                    n_elements_layer)

    # Job case
	# caseName = 'Caso_0_0_0_w2mm_lpro0p2mm_fine'

    # Set paths for directories
    basePath = f'{path}'
    outputPath = f'{basePath}/output/' + caseName
    if os.path.exists(outputPath):
        shutil.rmtree(f'{basePath}/output/' + caseName)
    os.makedirs(outputPath)
    outputMeshPath = f'{basePath}/output/' + caseName + '/msh/'
    os.makedirs(outputMeshPath)
    ##########################################
    ##########################################
    ##########################################
    ##########################################

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

    # 	fin = time.time()
    # 	tiempo_ej = fin-inicio
    # 	print(f"Tiempo de ejecución crear geometria y exportar: {tiempo_ej} segundos")

    print(f"    The model will have {(n_nodos - 1) * (n_nodos - 1) * (n_espesor - 1)} elements")

    ##########################################

    ##########################################

    # 	inicio =time.time()

    ###############################################################
    ###############################################################
    # Definir los valores iniciales y finales para discretización en X
    x0 = -Ldom / 2.0  # Primer valor
    xn = Ldom / 2.0  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_X = np.linspace(x0, xn, n_nodos)

    # Definir los valores iniciales y finales para discretización en Y
    y0 = -Ldom / 2.0  # Primer valor
    yn = Ldom / 2.0  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_Y = np.linspace(y0, yn, n_nodos)

    # Definir los valores iniciales y finales para discretización en Z
    z0 = 0.0  # Primer valor
    zn = n_layers * h_tow  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_Z = np.linspace(z0, zn, n_espesor)

    # Especifica las dimensiones de la matriz de 4 dimensiones
    dimX = int(n_nodos)  # Dimensión 1
    dimY = int(n_nodos)  # Dimensión 2
    dimZ = int(n_espesor)  # Dimensión 3
    dimCoord = 3  # Dimensión 4

    # Crea una matriz de 4 dimensiones llena de ceros
    matriz_4d = np.zeros((dimX, dimY, dimZ, dimCoord))
    # Llena la matriz con vector_equidistante_X sin bucles
    matriz_4d[:, :, 0, 0] = np.repeat(vector_equidistante_X[:, np.newaxis], dimX, axis=1)
    matriz_4d[:, :, 1:, 0] = matriz_4d[:, :, 0, 0][:, :, np.newaxis]

    matriz_4d[:, :, 0, 1] = np.repeat(vector_equidistante_Y[:, np.newaxis], dimY, axis=1).T
    matriz_4d[:, :, 1:, 1] = matriz_4d[:, :, 0, 1][:, :, np.newaxis]

    matriz_4d[:, 0, :, 2] = np.repeat(vector_equidistante_Z[:, np.newaxis], dimX, axis=1).T
    matriz_4d[:, 1:, :, 2] = matriz_4d[:, 0, :, 2][:, np.newaxis, :]

    ###############################################################
    ###############################################################
    # Ldom = 10.0
    nc = n_nodos - 1  # Número de puntos equidistantes, incluyendo x0 y xn
    n_espesorc = n_espesor - 1

    # Definir los valores iniciales y finales para discretización en X
    x0c = x0 + (Ldom / (n_nodos - 1)) / 2.0  # Primer valor
    xnc = xn - (Ldom / (n_nodos - 1)) / 2.0  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_Xc = np.linspace(x0c, xnc, nc)

    # Definir los valores iniciales y finales para discretización en Y
    y0c = y0 + (Ldom / (n_nodos - 1)) / 2.0  # Primer valor
    ync = yn - (Ldom / (n_nodos - 1)) / 2.0  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_Yc = np.linspace(y0c, ync, nc)

    # Definir los valores iniciales y finales para discretización en Z
    z0c = z0 + (n_layers * h_tow / (n_espesor - 1)) / 2.0  # Primer valor
    znc = zn - (n_layers * h_tow / (n_espesor - 1)) / 2.0  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_Zc = np.linspace(z0c, znc, n_espesorc)

    # Especifica las dimensiones de la matriz de 4 dimensiones
    dimXc = int(nc)  # Dimensión 1
    dimYc = int(nc)  # Dimensión 2
    dimZc = int(n_espesorc)  # Dimensión 3
    dimCoord = 3  # Dimensión 4

    # Crea una matriz de 4 dimensiones llena de ceros
    matriz_4dc = np.zeros((dimXc, dimYc, dimZc, dimCoord))
    # Llena la matriz con vector_equidistante_X sin bucles
    matriz_4dc[:, :, 0, 0] = np.repeat(vector_equidistante_Xc[:, np.newaxis], dimXc, axis=1)
    matriz_4dc[:, :, 1:, 0] = matriz_4dc[:, :, 0, 0][:, :, np.newaxis]

    matriz_4dc[:, :, 0, 1] = np.repeat(vector_equidistante_Yc[:, np.newaxis], dimYc, axis=1).T
    matriz_4dc[:, :, 1:, 1] = matriz_4dc[:, :, 0, 1][:, :, np.newaxis]

    matriz_4dc[:, 0, :, 2] = np.repeat(vector_equidistante_Zc[:, np.newaxis], dimXc, axis=1).T
    matriz_4dc[:, 1:, :, 2] = matriz_4dc[:, 0, :, 2][:, np.newaxis, :]

    # 	fin = time.time()
    # 	tiempo_ej = fin-inicio
    # 	print(f"Tiempo de ejecución discretizar nodos: {tiempo_ej} segundos")

    ###################################################################
    ###################################################################
    ###################################################################
    inicio = time.time()

    # Cargar el archivo STL en un objeto Trimesh
    mesh_loaded = []
    contarTow = 0

    for i in datos_input:
        contarTow += 1
        # Ruta del archivo de salida STL
        archivo_stl = outputPath + '/' + 'tow_{}.stl'.format(contarTow)
        mesh_loaded_n = trimesh.load(archivo_stl)
        mesh_loaded.append(mesh_loaded_n)
    # Verificar si el punto está dentro de la geometría
    matriz_3dc_oris = np.zeros((dimXc, dimYc, dimZc, 3))
    nodes = []
    for i in range(0, dimXc):
        for j in range(0, dimYc):
            for k in range(0, dimZc):
                nodes.append(np.array([[matriz_4dc[i, j, k, 0], matriz_4dc[i, j, k, 1], matriz_4dc[i, j, k, 2]]]))
    nodes = np.asarray(nodes, dtype=float)
    nodes = nodes[:, 0, :]
    tow_contains = []
    for tow in mesh_loaded:
        tow_contains.append(tow.contains(nodes))
    node_tows = np.zeros([len(tow_contains[0]), contarTow])
    for n, tow in enumerate(tow_contains):
        node_tows[:, n] = tow * (n + 1)

    # 	fin = time.time()
    # 	tiempo_ej = fin-inicio
    # 	print(f"Tiempo de ejecución asignar dentro/fuera: {tiempo_ej} segundos")

    # %%
    # 	inicio = time.time()
    matriz_1dc_inout = np.max(node_tows, axis=1)  # controla que tow quedarse en caso de que un nodo esté en varios
    matriz_3dc_inout = np.reshape(matriz_1dc_inout, [dimXc, dimYc, dimZc])

    for k in range(0, dimZc):
        for i in range(0, dimXc):
            for j in range(0, dimYc):
                point_to_check = np.array([[matriz_4dc[i, j, k, 0], matriz_4dc[i, j, k, 1], matriz_4dc[i, j, k, 2]]])
                if matriz_3dc_inout[i, j, k] != 0:
                    tow_orientacion = int(matriz_3dc_inout[i, j, k])

                    # Comprobar y añadir la orientacion
                    distance = []
                    delante_detras = []  # 1 indica delante, 0 indica detrás
                    for p in range(len(planos_Yarn[tow_orientacion - 1])):
                        A, B, C, D = planos_Yarn[tow_orientacion - 1][p][0:4]
                        distance.append(abs(A * point_to_check[0][0] + B * point_to_check[0][1] + C * point_to_check[0][
                            2] + D) / np.sqrt(A ** 2 + B ** 2 + C ** 2))

                        # Comprobar si está delante o detrás del plano
                        # Vector normal al plano
                        normal_vector = (A, B, C)
                        # Punto en el plano
                        x_plano = 0
                        y_plano = -D / B
                        z_plano = 0
                        p_plano = np.array([x_plano, y_plano, z_plano])

                        v_plano_point = np.array([point_to_check[0][0] - p_plano[0], point_to_check[0][1] - p_plano[1],
                                                  point_to_check[0][2] - p_plano[2]])

                        # Calcula el producto escalar
                        dot_product = sum(a * b for a, b in zip(normal_vector, v_plano_point))

                        # Determina si el punto está delante o detrás del plano
                        if dot_product >= 0:
                            delante_detras.append(1)
                        # print("El punto está delante del plano.")
                        else:
                            delante_detras.append(0)
                        # print("El punto está detrás del plano.")
                    # else: #si el punto está en el plano se le pone como si estuviera delante
                    #     delante_detras.append(1)
                    # print("El centroide {matriz_3dc_inout[i,j,k]} está en el plano.")

                    menor_distancia = min(distance)
                    posicion_menor = distance.index(menor_distancia)
                    delante_detras_menor = delante_detras[posicion_menor]

                    # Comprueba si hay un valor anterior al valor más bajo
                    if posicion_menor > 0:
                        posicion_anterior = posicion_menor - 1
                        delante_detras_anterior = delante_detras[posicion_anterior]
                    # valor_anterior = distance[posicion_menor - 1]
                    else:
                        posicion_anterior = None  # No hay valor anterior

                    # Comprueba si hay un valor posterior al valor más bajo
                    if posicion_menor < len(distance) - 1:
                        posicion_posterior = posicion_menor + 1
                        delante_detras_posterior = delante_detras[posicion_posterior]
                    # valor_posterior = distance[posicion_menor + 1]
                    else:
                        posicion_posterior = None  # No hay valor posterior

                    if posicion_anterior is not None and posicion_posterior is not None:
                        if delante_detras_menor != delante_detras_anterior:
                            P1 = np.array([centros_Yarn[tow_orientacion - 1][posicion_anterior]])
                            P2 = np.array([centros_Yarn[tow_orientacion - 1][posicion_menor]])
                            # Calcular la dirección desde P1 hacia P2
                            direccion = P2 - P1
                            # Normalizar la dirección para obtener un vector unitario
                            direccion_unitaria = direccion / np.linalg.norm(direccion)
                            # Asignar orientacion principal
                            matriz_3dc_oris[i, j, k, 0:3] = direccion_unitaria[0][0:3]
                        else:
                            P1 = np.array([centros_Yarn[tow_orientacion - 1][posicion_menor]])
                            P2 = np.array([centros_Yarn[tow_orientacion - 1][posicion_posterior]])
                            # Calcular la dirección desde P1 hacia P2
                            direccion = P2 - P1
                            # Normalizar la dirección para obtener un vector unitario
                            direccion_unitaria = direccion / np.linalg.norm(direccion)
                            # Asignar orientacion principal
                            matriz_3dc_oris[i, j, k, 0:3] = direccion_unitaria[0][0:3]
                    elif posicion_anterior is not None:
                        P1 = np.array([centros_Yarn[tow_orientacion - 1][posicion_anterior]])
                        P2 = np.array([centros_Yarn[tow_orientacion - 1][posicion_menor]])
                        # Calcular la dirección desde P1 hacia P2
                        direccion = P2 - P1
                        # Normalizar la dirección para obtener un vector unitario
                        direccion_unitaria = direccion / np.linalg.norm(direccion)
                        # Asignar orientacion principal
                        matriz_3dc_oris[i, j, k, 0:3] = direccion_unitaria[0][0:3]
                    elif posicion_posterior is not None:
                        P1 = np.array([centros_Yarn[tow_orientacion - 1][posicion_menor]])
                        P2 = np.array([centros_Yarn[tow_orientacion - 1][posicion_posterior]])
                        # Calcular la dirección desde P1 hacia P2
                        direccion = P2 - P1
                        # Normalizar la dirección para obtener un vector unitario
                        direccion_unitaria = direccion / np.linalg.norm(direccion)
                        # Asignar orientacion principal
                        matriz_3dc_oris[i, j, k, 0:3] = direccion_unitaria[0][0:3]
                    else:
                        print("Error. Revisar asignacion de orientacion")
                        sys.exit()  # Termina la ejecución del programa

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Geometry generation time: {round(tiempo_ej / 60, 2)} min")

    # %%

    # --------------------------------------------
    #
    # Borrar variables que no se van a utilizar
    #
    # --------------------------------------------

    del A, w_tow, angles_tows, archivo_stl, B, C, cent, centros_Yarn, comb
    del combined, contarTow, D, delante_detras, delante_detras_anterior, delante_detras_menor, delante_detras_posterior
    del dimCoord, direccion, direccion_unitaria, distance
    del dot_product, fin, i, inicio, j, k, L_pro, n, n_elements_layer, n_elements_gap
    del normal_vector, p, P1, P2, p_plano, plan, planos_Yarn, point_to_check, posicion_posterior
    del matriz_1dc_inout, menor_distancia, mesh_loaded, mesh_loaded_n, n_elements_towsingap, n_espesor
    del n_espesorc, n_nodos, n_tows, nc, node_tows, posicion_anterior, posicion_menor
    del tiempo_ej, tow, tow_contains, tow_orientacion, v_plano_point
    del vector_equidistante_X, vector_equidistante_Xc, vector_equidistante_Y, vector_equidistante_Yc
    del vector_equidistante_Z, vector_equidistante_Zc, x0, x0c, x_plano
    del xn, xnc, y0, y0c, y_plano, yn, ync, z0, z0c, z_plano, zn, znc

    # --------------------------------------------
    #
    # Alya files
    #
    # --------------------------------------------

    inicio = time.time()
    print('    Writting Alya files ...')
    print('    Writting Alya jobName.geo.dat ...')

    # Alya geo file
    gx = open(outputMeshPath + caseName + ".geo.dat", "w", newline='\n')
    #
    # Headers
    #
    # Alya geo file  (Section Nodes per element)
    gx.write("NODES_PER_ELEMENT")
    n_elems = dimXc * dimYc * dimZc
    for i in range(n_elems):
        # gx.write("\n   "+str(int(i)+1)+" "+str(n_elems[i]))
        gx.write("\n   " + str(int(i) + 1) + " " + str(int(8)))  # Los modelos siempre van a ser hexaedros
    gx.write("\nEND_NODES_PER_ELEMENT")

    # 	fin = time.time()
    # 	tiempo_ej = fin-inicio
    # 	print(f"Tiempo de ejecución nodos por elemento: {tiempo_ej} segundos")

    # 	inicio = time.time()
    # Alya geo file
    gx.write("\nELEMENTS")
    n_nodo = 1
    posicion_n_nodo = np.zeros((len(matriz_4d[:, 0, 0, 0]), len(matriz_4d[0, :, 0, 0]), len(matriz_4d[0, 0, :, 0])))
    for i in range(len(matriz_4d[:, 0, 0])):
        for j in range(len(matriz_4d[0, :, 0])):
            for k in range(len(matriz_4d[0, 0, :])):
                posicion_n_nodo[i, j, k] = n_nodo
                n_nodo = n_nodo + 1

    # 	fin = time.time()
    # 	tiempo_ej = fin-inicio
    # 	print(f"Tiempo de ejecución elementos primer bloque: {tiempo_ej} segundos")

    # 	inicio = time.time()
    Elementsetmaterials = np.zeros(
        (len(matriz_4dc[:, 0, 0, 0]) * len(matriz_4dc[0, :, 0, 0]) * len(matriz_4dc[0, 0, :, 0]), int(2)))
    Porosityfield_dir1_array = np.zeros(
        (len(matriz_4dc[:, 0, 0, 0]) * len(matriz_4dc[0, :, 0, 0]) * len(matriz_4dc[0, 0, :, 0]), int(3)))
    Porosityfield_dir2_array = np.zeros(
        (len(matriz_4dc[:, 0, 0, 0]) * len(matriz_4dc[0, :, 0, 0]) * len(matriz_4dc[0, 0, :, 0]), int(3)))
    element_node_conectivity = np.zeros(
        (len(matriz_4dc[:, 0, 0, 0]) * len(matriz_4dc[0, :, 0, 0]) * len(matriz_4dc[0, 0, :, 0]), int(9)))
    numero_elemento = np.zeros((len(matriz_4dc[:, 0, 0, 0]), len(matriz_4dc[0, :, 0, 0]), len(matriz_4dc[0, 0, :, 0])))
    n_elemento = 1
    for i in range(len(matriz_4dc[:, 0, 0])):
        for j in range(len(matriz_4dc[0, :, 0])):
            for k in range(len(matriz_4dc[0, 0, :])):
                e0 = str(int(n_elemento))
                e1 = str(int(posicion_n_nodo[i, j, k]))
                e2 = str(int(posicion_n_nodo[i + 1, j, k]))
                e3 = str(int(posicion_n_nodo[i + 1, j + 1, k]))
                e4 = str(int(posicion_n_nodo[i, j + 1, k]))
                e5 = str(int(posicion_n_nodo[i, j, k + 1]))
                e6 = str(int(posicion_n_nodo[i + 1, j, k + 1]))
                e7 = str(int(posicion_n_nodo[i + 1, j + 1, k + 1]))
                e8 = str(int(posicion_n_nodo[i, j + 1, k + 1]))
                gx.write(f"\n  {e0} {e1} {e2} {e3} {e4} {e5} {e6} {e7} {e8}  ")
                element_node_conectivity[n_elemento - 1, :] = [e0, e1, e2, e3, e4, e5, e6, e7, e8]
                if int(matriz_3dc_inout[i, j, k]) != 0:
                    Elementsetmaterials[n_elemento - 1, :] = [n_elemento, 2]
                else:
                    Elementsetmaterials[n_elemento - 1, 0] = n_elemento
                numero_elemento[i, j, k] = n_elemento
                Porosityfield_dir1_array[n_elemento - 1, :] = [matriz_3dc_oris[i, j, k, 0], matriz_3dc_oris[i, j, k, 1],
                                                               matriz_3dc_oris[i, j, k, 2]]
                # Genera un vector aleatorio
                vector_aleatorio = np.random.rand(3)
                proyeccion = np.dot(vector_aleatorio, matriz_3dc_oris[i, j, k, :]) * matriz_3dc_oris[i, j, k, :]
                vector_ortogonal = vector_aleatorio - proyeccion
                # Normaliza el vector ortogonal
                Porosityfield_dir2_array[n_elemento - 1, :] = vector_ortogonal / np.linalg.norm(vector_ortogonal)
                n_elemento = n_elemento + 1
    Porosityfield_dir3_array = np.cross(Porosityfield_dir1_array, Porosityfield_dir2_array)

    # Alya geo file (End Section elements)
    gx.write("\nEND_ELEMENTS")
    del n_elemento, n_nodo, e0, e1, e2, e3, e4, e5, e6, e7, e8

    # 	fin = time.time()
    # 	tiempo_ej = fin-inicio
    # 	print(f"Tiempo de ejecución elementos segundo bloque: {tiempo_ej} segundos")

    # 	inicio = time.time()
    # Alya geo file (Section coordinates)
    gx.write("\nCOORDINATES")
    n_nodo = 1
    for i in range(len(matriz_4d[:, 0, 0, 0])):
        for j in range(len(matriz_4d[0, :, 0, 0])):
            for k in range(len(matriz_4d[0, 0, :, 0])):
                coor_x = np.format_float_scientific(matriz_4d[i, j, k, 0], precision=6)
                coor_y = np.format_float_scientific(matriz_4d[i, j, k, 1], precision=6)
                coor_z = np.format_float_scientific(matriz_4d[i, j, k, 2], precision=6)
                gx.write(f"\n     {n_nodo}   {coor_x}  {coor_y}  {coor_z}   ")
                n_nodo = n_nodo + 1

    # Alya geo file (End Section coordinates)
    gx.write("\nEND_COORDINATES")
    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Geo file generation time: {round(tiempo_ej / 60, 2)} min")

    # Alya geo file (End file)
    gx.close()

    # --------------------------------------------
    #
    # Alya .mat.dat
    # The number of materials is harcoded to be always 2: fibre and matrix
    # --------------------------------------------
    inicio = time.time()
    print('    Writting Alya jobName.mat.dat ...')
    nmate = writeAlyaMat(outputMeshPath, caseName, Elementsetmaterials)
    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Mat file generation time: {round(tiempo_ej / 60, 2)} min")
    # --------------------------------------------
    #
    # Alya .bou.dat and .fix.dat
    #
    # --------------------------------------------
    inicio = time.time()

    # 	print('Getting Alya boundaries ...')
    print('    Writting Alya jobName.bou.dat ...')

    # e1list = [int(numero_elemento[0][j][k]) for j in range(len(numero_elemento[0])) for k in range(len(numero_elemento[0][j]))]
    # e2list = [int(numero_elemento[-1][j][k]) for j in range(len(numero_elemento[-1])) for k in range(len(numero_elemento[-1][j]))]
    # e3list = [int(numero_elemento[i][0][k]) for i in range(len(numero_elemento)) for k in range(len(numero_elemento[i][0]))]
    # e4list = [int(numero_elemento[i][-1][k]) for i in range(len(numero_elemento)) for k in range(len(numero_elemento[i][-1]))]
    # e5list = [int(numero_elemento[i][j][0]) for i in range(len(numero_elemento)) for j in range(len(numero_elemento[i]))]
    # e6list = [int(numero_elemento[i][j][-1]) for i in range(len(numero_elemento)) for j in range(len(numero_elemento[i]))]
    # x0 = [int(posicion_n_nodo[0][j][k]) for j in range(len(posicion_n_nodo[0])) for k in range(len(posicion_n_nodo[0][j]))]
    # xl = [int(posicion_n_nodo[-1][j][k]) for j in range(len(posicion_n_nodo[-1])) for k in range(len(posicion_n_nodo[-1][j]))]
    # y0 = [int(posicion_n_nodo[i][0][k]) for i in range(len(posicion_n_nodo)) for k in range(len(posicion_n_nodo[i][0]))]
    # yl = [int(posicion_n_nodo[i][-1][k]) for i in range(len(posicion_n_nodo)) for k in range(len(posicion_n_nodo[i][-1]))]
    # z0 = [int(posicion_n_nodo[i][j][0]) for i in range(len(posicion_n_nodo)) for j in range(len(posicion_n_nodo[i]))]
    # zl = [int(posicion_n_nodo[i][j][-1]) for i in range(len(posicion_n_nodo)) for j in range(len(posicion_n_nodo[i]))]
    # blist = [[e1list,x0], [e2list,xl], [e3list,y0], [e4list,yl], [e5list,z0], [e6list,zl]]

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

    # Built RVE element boundaries for each boundary
    # b_list, nboun = getRVEboundaries(element_node_conectivity,blist)

    # 	fin = time.time()
    # 	tiempo_ej = fin-inicio
    # 	print(f"Tiempo de ejecución getRVEboundaries: {tiempo_ej} segundos")
    # 	inicio = time.time()

    writeAlyaBou(outputMeshPath, caseName, b_list)
    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Bou file generation time: {round(tiempo_ej / 60, 2)} min")
    inicio = time.time()

    print('    Writting Alya jobName.fix.dat ...')
    writeAlyaFix(outputMeshPath, caseName, b_list)

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
    # inicio = time.time()

    # print('Reading .ori file ...')

    # # importa el archivo .ori y se analiza la orientación de todos los elementos para luego asignar la permeabilidad

    # fin = time.time()
    # tiempo_ej = fin-inicio
    # print(f"Tiempo de ejecución crear variables de orientaciones: {tiempo_ej} segundos")
    inicio = time.time()

    print('    Writting Alya jobName.fie.dat ...')
    writeAlyaFie(outputMeshPath, caseName, viscosity, k_lon, k_per, Elementsetmaterials, \
                 numerodeelementos, Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array)

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Fie file generation time: {round(round(tiempo_ej / 60, 2))} min")

    # --------------------------------------------
    #
    # from Escritura_inp import Escritura_inp
    # Escritura_inp(nombre_case ,dimX, dimY, dimZ, matriz_4d, dimXc, dimYc, dimZc, datos_input, matriz_3dc_inout, matriz_3dc_oris,
    #                Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array)
    # #
    # --------------------------------------------

    # --------------------------------------------
    #
    # Alya Set - BSC (mesh) - estamos machacando el otro de momento
    #
    # --------------------------------------------
    #### AQUÍ ABRÍA QUE INCLUIR LA PARTE DE LOS SETS
    ####
    ####
    ####
    ####
    inicio = time.time()

    print('    Writting Alya jobName.set.dat ...')

    # Alya Set
    if AlyaSet == 'All':
        writeAlyaSet(outputMeshPath, caseName, numerodeelementos, numerodeboundelems)
    else:
        writeAlyaSet2(outputMeshPath, caseName, Lset, n_layers, nodes)
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
        # Get nodes from vertices
        n1, n2, n3, n4, n5, n6, n7, n8 = getRVEnodesFromVertices(lx, ly, lz, na, n)

        # Get nodes from edges
        e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12 = getRVEnodesFromEdges(lx, ly, lz, n, na, n1, n2, n3, n4, n5,
                                                                                 n6, n7, n8)

        bound_xl = e1 + e2 + e5 + e6 + [n1] + [n2] + [n3] + [n4]
        bound_yl = e2 + e3 + e10 + e11 + [n2] + [n3] + [n6] + [n7]
        bound_zl = e6 + e7 + e11 + e12 + [n3] + [n4] + [n7] + [n8]

        # Slave - master approach
        lmast = []
        print('Adding nodes from vertices ...')
        lmast = addNodesFromVertices(n1, n2, n3, n4, n5, n6, n7, n8, lmast)

        print('Adding nodes from edges ...')
        lmast = addNodesFromEdges(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, x, y, z, tol, lmast)

        print('Adding nodes from faces ...')
        fileName = 'x'
        lmast = addNodesFromFacesMeso('x', x, y, z, x0, y0, z0, xl, yl, zl, bound_xl, bound_yl, bound_zl, tol, lmast)
        lmast.sort(key=lambda k: k[0])
        print('Writting Alya jobName.per.dat ...')
        writeAlyaPer(path, fileName, lmast)
        if 'y' in simulaciones:
            shutil.copy("x.per.dat", "y.per.dat")
        if 'z' in simulaciones:
            fileName = 'z'
            lmast = addNodesFromFacesMeso('z', x, y, z, x0, y0, z0, xl, yl, zl, bound_xl, bound_yl, bound_zl, tol,
                                          lmast)
            lmast.sort(key=lambda k: k[0])
            print('Writting Alya jobName.per.dat ...')
            writeAlyaPer(path, fileName, lmast)
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
    lz = n_layers * h_tow  # Esto son mm
    length = [lx * 1e-3, ly * 1e-3, lz * 1e-3]  # TODO: Acordar las unidades y quitar!
    for j in range(len(simulaciones)):
        path = outputPath + '/' + str(simulaciones[j]) + '/'
        os.makedirs(path)
        fileName = caseName
        icase = str(simulaciones[j])

        node = 1  # TODO: Coger un nodo que no este en la direccion del flow (solo en z)
        # Preliminary calculations
        #		gravity = Presion_de_inyeccion/(density*length[j])
        Presion_de_inyeccion = gravity * (density * length[j])

        # Alya Dom
        writeAlyaDom(path, fileName, icase, int(numerodenodos), numerodeelementos, numerodeboundelems, nmate,
                     periodicityMethod, fieldFlag)
        # Alya Dat
        writeAlyaDat(debug, path, fileName, TotalTimeSimulation, MaxNumSteps)
        # Alya Ker
        writeAlyaKer(debug, path, fileName, nmate, density, viscosity)
        # Alya Nsi
        writeAlyaNsi(debug, path, fileName, icase, Presion_de_inyeccion, gravity, lx, ly, lz, node)
        # Alya Pos
        writeAlyaPos(path, fileName)

        # Job Launcher
        writeJobLauncher(path, fileName, queue, numCPUs)

    # Get the end time
    et = time.time()

    # Get the execution time
    elapsed_time = et - st

    fin = time.time()
    tiempo_ej = fin - inicio
    print(f"        Geo file generation time: {round(elapsed_time / 60, 2)} min")
    print('  Total execution time:', round(elapsed_time / 60, 2), 'min')
