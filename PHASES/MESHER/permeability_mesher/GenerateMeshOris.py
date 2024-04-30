import numpy as np
import trimesh
import sys

def Mesh_and_Oris(Ldom, n_nodos,n_capas, h_tow, n_espesor, datos_input, outputPath, planos_Yarn, centros_Yarn):
    ###############################################################
    ###############################################################
    # Definir los valores iniciales y finales para discretización en X
    x0 = -Ldom/2.0  # Primer valor
    xn = Ldom/2.0  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_X = np.linspace(x0, xn, n_nodos)

    # Definir los valores iniciales y finales para discretización en Y
    y0 = -Ldom/2.0  # Primer valor
    yn = Ldom/2.0  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_Y = np.linspace(y0, yn, n_nodos)

    # Definir los valores iniciales y finales para discretización en Z
    z0 = 0.0  # Primer valor
    zn = n_capas*h_tow  # Último valor

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
    nc = n_nodos-1  # Número de puntos equidistantes, incluyendo x0 y xn
    n_espesorc = n_espesor-1

    # Definir los valores iniciales y finales para discretización en X
    x0c = x0+(Ldom/(n_nodos-1))/2.0  # Primer valor
    xnc = xn-(Ldom/(n_nodos-1))/2.0  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_Xc = np.linspace(x0c, xnc, nc)

    # Definir los valores iniciales y finales para discretización en Y
    y0c = y0+(Ldom/(n_nodos-1))/2.0  # Primer valor
    ync = yn-(Ldom/(n_nodos-1))/2.0  # Último valor

    # Crear el vector de puntos equidistantes
    vector_equidistante_Yc = np.linspace(y0c, ync, nc)

    # Definir los valores iniciales y finales para discretización en Z
    z0c = z0+(n_capas*h_tow/(n_espesor-1))/2.0  # Primer valor
    znc = zn-(n_capas*h_tow/(n_espesor-1))/2.0  # Último valor

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
    print("Mesh_and_Oris 6")

    for i in range(0,dimXc):
        for j in range(0,dimYc):
            for k in range(0,dimZc):
                print(f"Mesh_and_Oris {i} {j} {k}")
                nodes.append(np.array([[matriz_4dc[i,j,k,0], matriz_4dc[i,j,k,1], matriz_4dc[i,j,k,2]]]))
    nodes = np.asarray(nodes, dtype = float)
    nodes = nodes[:,0,:]
    tow_contains = []
    for tow in mesh_loaded:
        tow_contains.append(tow.contains(nodes))
    node_tows = np.zeros([len(tow_contains[0]),contarTow])
    for n, tow in enumerate(tow_contains):
        node_tows[:,n] = tow*(n+1)

    
# 	fin = time.time()
# 	tiempo_ej = fin-inicio
# 	print(f"Tiempo de ejecución asignar dentro/fuera: {tiempo_ej} segundos")    

    #%%
# 	inicio = time.time() 
    matriz_1dc_inout = np.max(node_tows, axis = 1) #controla que tow quedarse en caso de que un nodo esté en varios
    matriz_3dc_inout = np.reshape(matriz_1dc_inout, [dimXc, dimYc, dimZc])

    for i in range(1,dimXc-1):
        for j in range(1,dimYc-1):
            for k in range(1,dimZc-1):
                if (matriz_3dc_inout[i-1, j-1, k] and matriz_3dc_inout[i-1, j, k] and matriz_3dc_inout[i-1, j+1, k] and
                    matriz_3dc_inout[i, j-1, k] and matriz_3dc_inout[i, j, k] and matriz_3dc_inout[i, j+1, k] and
                    matriz_3dc_inout[i+1, j-1, k] and matriz_3dc_inout[i+1, j, k] and matriz_3dc_inout[i+1, j+1, k]) == 0:
                    if (matriz_3dc_inout[i-1, j-1, k-1] and matriz_3dc_inout[i-1, j, k-1] and matriz_3dc_inout[i-1, j+1, k-1] and
                        matriz_3dc_inout[i, j-1, k-1] and matriz_3dc_inout[i, j, k-1] and matriz_3dc_inout[i, j+1, k-1] and
                        matriz_3dc_inout[i+1, j-1, k-1] and matriz_3dc_inout[i+1, j, k-1] and matriz_3dc_inout[i+1, j+1, k-1] and
                        matriz_3dc_inout[i-1, j-1, k+1] and matriz_3dc_inout[i-1, j, k+1] and matriz_3dc_inout[i-1, j+1, k+1] and 
                        matriz_3dc_inout[i, j-1, k+1] and matriz_3dc_inout[i, j, k+1] and matriz_3dc_inout[i, j+1, k+1] and
                        matriz_3dc_inout[i+1, j-1, k+1] and matriz_3dc_inout[i+1, j, k+1] and matriz_3dc_inout[i+1, j+1, k+1]) != 0:
                        matriz_3dc_inout[i-1, j-1, k] = matriz_3dc_inout[i-1, j-1, k+1]
                        matriz_3dc_inout[i-1, j, k] = matriz_3dc_inout[i-1, j, k+1]
                        matriz_3dc_inout[i-1, j+1, k] = matriz_3dc_inout[i-1, j+1, k+1]
                        matriz_3dc_inout[i, j-1, k] = matriz_3dc_inout[i, j-1, k+1]
                        matriz_3dc_inout[i, j, k] = matriz_3dc_inout[i, j, k+1]
                        matriz_3dc_inout[i, j+1, k] = matriz_3dc_inout[i, j+1, k+1]
                        matriz_3dc_inout[i+1, j-1, k] = matriz_3dc_inout[i+1, j-1, k+1]
                        matriz_3dc_inout[i+1, j, k] = matriz_3dc_inout[i+1, j, k+1]
                        matriz_3dc_inout[i+1, j+1, k] = matriz_3dc_inout[i+1, j+1, k+1]

    print("Mesh_and_Oris 8")

    for k in range(0,dimZc):
        for i in range(0,dimXc):
            for j in range(0,dimYc):
                point_to_check = np.array([[matriz_4dc[i,j,k,0], matriz_4dc[i,j,k,1], matriz_4dc[i,j,k,2]]])
                if matriz_3dc_inout[i,j,k] != 0:
                    tow_orientacion = int(matriz_3dc_inout[i,j,k])

                    # Comprobar y añadir la orientacion
                    distance = []
                    delante_detras = [] #1 indica delante, 0 indica detrás
                    for p in range(len(planos_Yarn[tow_orientacion-1])):
                        A,B,C,D = planos_Yarn[tow_orientacion-1][p][0:4]
                        distance.append(abs(A * point_to_check[0][0] + B * point_to_check[0][1] + C * point_to_check[0][2] + D) / np.sqrt(A**2 + B**2 + C**2))

                        #Comprobar si está delante o detrás del plano
                        # Vector normal al plano
                        normal_vector = (A, B, C)
                        # Punto en el plano
                        if B != 0:
                            x_plano = 0
                            y_plano = -D/B
                            z_plano = 0
                        else:
                            x_plano = -D/A
                            y_plano = 0
                            z_plano = 0
                        p_plano = np.array([x_plano, y_plano, z_plano])

                        v_plano_point = np.array([point_to_check[0][0]-p_plano[0], point_to_check[0][1]-p_plano[1], point_to_check[0][2]-p_plano[2]])

                        # Calcula el producto escalar
                        dot_product = sum(a * b for a, b in zip(normal_vector, v_plano_point))

                        # Determina si el punto está delante o detrás del plano
                        if dot_product >= 0:
                            delante_detras.append(1)
                            #print("El punto está delante del plano.")
                        else:
                            delante_detras.append(0)
                            #print("El punto está detrás del plano.")
                        # else: #si el punto está en el plano se le pone como si estuviera delante
                        #     delante_detras.append(1)
                            #print("El centroide {matriz_3dc_inout[i,j,k]} está en el plano.")

                    menor_distancia = min(distance)
                    posicion_menor = distance.index(menor_distancia)
                    delante_detras_menor = delante_detras[posicion_menor]


                    # Comprueba si hay un valor anterior al valor más bajo
                    if posicion_menor > 0:
                        posicion_anterior = posicion_menor - 1
                        delante_detras_anterior = delante_detras[posicion_anterior]
                        #valor_anterior = distance[posicion_menor - 1]
                    else:
                        posicion_anterior = None  # No hay valor anterior

                    # Comprueba si hay un valor posterior al valor más bajo
                    if posicion_menor < len(distance) - 1:
                        posicion_posterior = posicion_menor + 1
# 						delante_detras_posterior = delante_detras[posicion_posterior]
                        #valor_posterior = distance[posicion_menor + 1]
                    else:
                        posicion_posterior = None  # No hay valor posterior


                    if posicion_anterior is not None and posicion_posterior is not None:
                        if delante_detras_menor != delante_detras_anterior:
                            P1 = np.array([centros_Yarn[tow_orientacion-1][posicion_anterior]])
                            P2 = np.array([centros_Yarn[tow_orientacion-1][posicion_menor]])
                            # Calcular la dirección desde P1 hacia P2
                            direccion = P2 - P1
                            # Normalizar la dirección para obtener un vector unitario
                            direccion_unitaria = direccion / np.linalg.norm(direccion)
                            # Asignar orientacion principal
                            matriz_3dc_oris[i, j, k, 0:3] = direccion_unitaria[0][0:3]
                        else:
                            P1 = np.array([centros_Yarn[tow_orientacion-1][posicion_menor]])
                            P2 = np.array([centros_Yarn[tow_orientacion-1][posicion_posterior]])
                            # Calcular la dirección desde P1 hacia P2
                            direccion = P2 - P1
                            # Normalizar la dirección para obtener un vector unitario
                            direccion_unitaria = direccion / np.linalg.norm(direccion)
                            # Asignar orientacion principal
                            matriz_3dc_oris[i, j, k, 0:3] = direccion_unitaria[0][0:3]
                    elif posicion_anterior is not None:
                        P1 = np.array([centros_Yarn[tow_orientacion-1][posicion_anterior]])
                        P2 = np.array([centros_Yarn[tow_orientacion-1][posicion_menor]])
                        # Calcular la dirección desde P1 hacia P2
                        direccion = P2 - P1
                        # Normalizar la dirección para obtener un vector unitario
                        direccion_unitaria = direccion / np.linalg.norm(direccion)
                        # Asignar orientacion principal
                        matriz_3dc_oris[i, j, k, 0:3] = direccion_unitaria[0][0:3]
                    elif posicion_posterior is not None:
                        P1 = np.array([centros_Yarn[tow_orientacion-1][posicion_menor]])
                        P2 = np.array([centros_Yarn[tow_orientacion-1][posicion_posterior]])
                        # Calcular la dirección desde P1 hacia P2
                        direccion = P2 - P1
                        # Normalizar la dirección para obtener un vector unitario
                        direccion_unitaria = direccion / np.linalg.norm(direccion)
                        # Asignar orientacion principal
                        matriz_3dc_oris[i, j, k, 0:3] = direccion_unitaria[0][0:3]
                    else:
                        print("Error. Revisar asignacion de orientacion")
                        sys.exit()  # Termina la ejecución del programa

    return dimXc, dimYc, dimZc, matriz_4d, matriz_4dc, matriz_3dc_inout, matriz_3dc_oris, nodes
