import numpy as np
import trimesh
from numba import jit


def Mesh_and_Oris(Ldom, n_nodos,n_capas, h_tow, n_espesor, datos_input, outputPath, planos_Yarn, centros_Yarn):
	
	##############################################################
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
    

    
	for i in range(0,dimXc):
		for j in range(0,dimYc):
			for k in range(0,dimZc):
				nodes.append(np.array([[matriz_4dc[i,j,k,0], matriz_4dc[i,j,k,1], matriz_4dc[i,j,k,2]]]))
	nodes = np.asarray(nodes, dtype = float)
	nodes = nodes[:,0,:]
    
    
	# Inicializar una matriz para almacenar el índice del tow que contiene cada nodo
	matriz_1dc_inout = np.zeros(len(nodes), dtype=int)

	# Iterar sobre cada tow y actualizar matriz_1dc_inout
	for n, tow in enumerate(mesh_loaded):
	    contains = tow.contains(nodes)  # Esto devuelve un array booleano
	    matriz_1dc_inout[contains] = n + 1  # Actualizar los nodos contenidos por el tow actual, controlando qué nodo quedarse en caos de que esté en varios


	#%%
	#inicio = time.time()

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
    
    
    
    # Precomputar constantes que se utilizan repetidamente
	planos_Yarn_normalized = []
	for planos in planos_Yarn:
	    planos_Yarn_normalized.append([
	        (A, B, C, D, np.sqrt(A**2 + B**2 + C**2)) for (A, B, C, D) in planos
	    ])
        
    
    
	def precompute_planos_normalized(planos_Yarn):
	    max_planes = max(len(planos) for planos in planos_Yarn)
	    planos_Yarn_normalized = np.zeros((len(planos_Yarn), max_planes, 6))
	    for i, planos in enumerate(planos_Yarn):
	        for j, (A, B, C, D) in enumerate(planos):
	            normalizer = np.sqrt(A**2 + B**2 + C**2)
	            planos_Yarn_normalized[i, j] = (A, B, C, D, normalizer, j+1)
	    return planos_Yarn_normalized
	
	def convert_centros_yarn(centros_Yarn):
	    max_len = max(len(c) for c in centros_Yarn)
	    array_yarn = np.zeros((len(centros_Yarn), max_len, 3))
	    for i, c in enumerate(centros_Yarn):
	        for j, centro in enumerate(c):
	            array_yarn[i, j, :] = centro
	    return array_yarn
	
	@jit(nopython=True)
	def calcular_orientacion(matriz_3dc_inout, matriz_4dc, centros_Yarn, planos_Yarn_normalized, dimXc, dimYc, dimZc):
	    matriz_3dc_oris = np.zeros((dimXc, dimYc, dimZc, 3))
	    
	    for k in range(dimZc):
	        for i in range(dimXc):
	            for j in range(dimYc):
	                if matriz_3dc_inout[i, j, k] != 0:
	                    point_to_check = matriz_4dc[i, j, k, :3]
	                    tow_orientacion = int(matriz_3dc_inout[i, j, k]) - 1
	                    
	                    # Inicializar listas para distancias y posiciones relativas
	                    num_planes = int(max(planos_Yarn_normalized[tow_orientacion,:,5]))
	                    distances = np.zeros(num_planes)
	                    delante_detras = np.zeros(num_planes, dtype=np.int32)
		                    
	                    # Calcular distancias y posiciones relativas para cada plano
	                    for idx in range(num_planes):
	                        A, B, C, D, normalizer, nplano = planos_Yarn_normalized[tow_orientacion][idx]
	                        distance = abs(A * point_to_check[0] + B * point_to_check[1] + C * point_to_check[2] + D) / normalizer
	                        distances[idx] = distance
	                        dot_product = A * point_to_check[0] + B * point_to_check[1] + C * point_to_check[2] + D
	                        delante_detras[idx] = 1 if dot_product >= 0 else 0
	                    
	                    # Encontrar la menor distancia y su posición
	                    min_distance = np.inf
	                    posicion_menor = -1
	                    for idx in range(num_planes):
	                        if distances[idx] < min_distance:
	                            min_distance = distances[idx]
	                            posicion_menor = idx
	                    delante_detras_menor = delante_detras[posicion_menor]
	                    
	                    # Determinar posiciones anteriores y posteriores
	                    posicion_anterior = posicion_menor - 1 if posicion_menor > 0 else -1
	                    posicion_posterior = posicion_menor + 1 if posicion_menor < num_planes - 1 else -1
	                    
	                    # Calcular la dirección unitaria principal
	                    if posicion_anterior != -1 and posicion_posterior != -1:
	                        if delante_detras_menor != delante_detras[posicion_anterior]:
	                            P1 = centros_Yarn[tow_orientacion, posicion_anterior]
	                            P2 = centros_Yarn[tow_orientacion, posicion_menor]
	                        else:
	                            P1 = centros_Yarn[tow_orientacion, posicion_menor]
	                            P2 = centros_Yarn[tow_orientacion, posicion_posterior]
	                    elif posicion_anterior != -1:
	                        P1 = centros_Yarn[tow_orientacion, posicion_anterior]
	                        P2 = centros_Yarn[tow_orientacion, posicion_menor]
	                    elif posicion_posterior != -1:
	                        P1 = centros_Yarn[tow_orientacion, posicion_menor]
	                        P2 = centros_Yarn[tow_orientacion, posicion_posterior]
	                    else:
	                        raise ValueError("Error. Revisar asignacion de orientacion")
                            
	                    
	                    # Normalizar la dirección para obtener un vector unitario
	                    direccion = P2 - P1
	                    direccion_unitaria = direccion / np.linalg.norm(direccion)
                        
	                    
	                    # Asignar orientación principal
	                    matriz_3dc_oris[i, j, k, :3] = direccion_unitaria
	    
	    return matriz_3dc_oris
	
	# Convertir centros_Yarn y planos_Yarn a arrays de NumPy
	centros_Yarn_np = convert_centros_yarn(centros_Yarn)
	planos_Yarn_normalized = precompute_planos_normalized(planos_Yarn)
	
	# Calcular la orientación
	matriz_3dc_oris = calcular_orientacion(matriz_3dc_inout, matriz_4dc, centros_Yarn_np, planos_Yarn_normalized, dimXc, dimYc, dimZc)


	return dimXc, dimYc, dimZc, matriz_4d, matriz_4dc, matriz_3dc_inout, matriz_3dc_oris, nodes
	