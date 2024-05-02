import numpy as np

def proyectar_en_plano(vector, normal):
    """
    Proyecta un vector en el plano definido por una normal.
    
    Parámetros:
    vector: np.array - Vector a proyectar.
    normal: np.array - Normal del plano.
    
    Retorna:
    np.array - Vector proyectado en el plano.
    """
    return vector - np.dot(vector, normal) * normal / np.linalg.norm(normal)**2

def calcular_angulo_entre_vectores(v1, v2):
    """
    Calcula el ángulo entre dos vectores.
    
    Parámetros:
    v1: np.array - Primer vector.
    v2: np.array - Segundo vector.
    
    Retorna:
    float - Ángulo en radianes entre los dos vectores.
    """
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        angulo = np.nan
    else:
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angulo = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    return angulo

def writeAlyaGeo(outputMeshPath, caseName, dimXc, dimYc, dimZc, matriz_4d, matriz_4dc, matriz_3dc_inout, matriz_3dc_oris, angulos_tows, n_elementos_capa, matriz_3dc_FVF):
# Alya geo file
    gx=open(outputMeshPath + caseName + ".geo.dat","w", newline='\n')
    #
    # Headers
    #
    # Alya geo file  (Section Nodes per element)
    gx.write("NODES_PER_ELEMENT")
    n_elems = dimXc*dimYc*dimZc
    for i in range(n_elems):
        print(f"THIRD LOOP {i} out of dimXc {n_elems}")
        #gx.write("\n   "+str(int(i)+1)+" "+str(n_elems[i]))
        gx.write("\n   "+str(int(i)+1)+" "+str(int(8)))  # Los modelos siempre van a ser hexaedros
    gx.write("\nEND_NODES_PER_ELEMENT")

# 	fin = time.time()
# 	tiempo_ej = fin-inicio
# 	print(f"Tiempo de ejecución nodos por elemento: {tiempo_ej} segundos") 

# 	inicio = time.time()
    # Alya geo file
    gx.write("\nELEMENTS")
    n_nodo = 1
    posicion_n_nodo = np.zeros((len(matriz_4d[:,0,0,0]), len(matriz_4d[0,:,0,0]), len(matriz_4d[0,0,:,0])))
    for i in range(len(matriz_4d[:,0,0])):
        print(f"THIRD LOOP {i} out of matriz_4d {(len(matriz_4d[:,0,0]))}")
        for j in range(len(matriz_4d[0,:,0])):
            for k in range(len(matriz_4d[0,0,:])):
                posicion_n_nodo[i,j,k]=n_nodo
                n_nodo = n_nodo + 1

# 	fin = time.time()
# 	tiempo_ej = fin-inicio
# 	print(f"Tiempo de ejecución elementos primer bloque: {tiempo_ej} segundos") 


# 	inicio = time.time()
    Elementsetmaterials = np.zeros((len(matriz_4dc[:,0,0,0]) * len(matriz_4dc[0,:,0,0]) * len(matriz_4dc[0,0,:,0]), int(3)))
    Porosityfield_dir1_array = np.zeros((len(matriz_4dc[:,0,0,0]) * len(matriz_4dc[0,:,0,0]) * len(matriz_4dc[0,0,:,0]), int(3)))
    Porosityfield_dir2_array = np.zeros((len(matriz_4dc[:,0,0,0]) * len(matriz_4dc[0,:,0,0]) * len(matriz_4dc[0,0,:,0]), int(3)))
    element_node_conectivity = np.zeros((len(matriz_4dc[:,0,0,0]) * len(matriz_4dc[0,:,0,0]) * len(matriz_4dc[0,0,:,0]), int(9)))
    numero_elemento = np.zeros((len(matriz_4dc[:,0,0,0]), len(matriz_4dc[0,:,0,0]), len(matriz_4dc[0,0,:,0])))
    n_elemento = 1
    for i in range(len(matriz_4dc[:,0,0])):
        print(f"5 LOOP {i} out of matriz_4d {(len(matriz_4d[:, 0, 0]))}")
        for j in range(len(matriz_4dc[0,:,0])):
            for k in range(len(matriz_4dc[0,0,:])):
                e0 = str(int(n_elemento))
                e1 = str(int(posicion_n_nodo[i, j, k]))
                e2 = str(int(posicion_n_nodo[i+1, j, k]))
                e3 = str(int(posicion_n_nodo[i+1, j+1, k]))
                e4 = str(int(posicion_n_nodo[i, j+1, k]))
                e5 = str(int(posicion_n_nodo[i, j, k+1]))
                e6 = str(int(posicion_n_nodo[i+1, j, k+1]))
                e7 = str(int(posicion_n_nodo[i+1, j+1, k+1]))
                e8 = str(int(posicion_n_nodo[i, j+1, k+1]))
                gx.write(f"\n  {e0} {e1} {e2} {e3} {e4} {e5} {e6} {e7} {e8}  ")
                element_node_conectivity [n_elemento-1, :] = [e0,e1,e2,e3,e4,e5,e6,e7,e8]
                FVF = matriz_3dc_FVF[i,j,k]
                if int(matriz_3dc_inout[i,j,k]) != 0:
                    Elementsetmaterials[n_elemento-1, :] = [n_elemento, 2, FVF]
                else:
                    if FVF != 0:
                        print()
                        print('#########################')
                        print('NO COINCIDE FVF CON MATERIAL')
                        print('VER WriteAlyaGeo')
                        print('#########################')
                        print()
                    Elementsetmaterials[n_elemento-1, 0] = n_elemento
                numero_elemento[i,j,k] = n_elemento
                Porosityfield_dir1_array[n_elemento-1,:] = [matriz_3dc_oris[i,j,k,0], matriz_3dc_oris[i,j,k,1], matriz_3dc_oris[i,j,k,2]]
                
                dir_orientacion_0 = np.array([0, 1, 0])
                u3 = np.array([0, 0, 1])
                # Proyectar t y n en el plano definido por u3
                longitudinal_proyectado = proyectar_en_plano(Porosityfield_dir1_array[n_elemento-1,:], u3)
                dir0_proyectado = proyectar_en_plano(dir_orientacion_0, u3)
                # Calcular el ángulo entre los vectores proyectados
                angulo = np.degrees(calcular_angulo_entre_vectores(longitudinal_proyectado, dir0_proyectado))
                
                if np.isnan(angulo) == False:
                    angulo_mas90 = int(angulo+90)
                    vector_mas90 = np.array([np.cos(np.deg2rad(angulo_mas90)),np.sin(np.deg2rad(angulo_mas90)),0])
                    proyeccion = np.dot(vector_mas90, matriz_3dc_oris[i, j, k, :]) * matriz_3dc_oris[i, j, k, :]
                    vector_ortogonal = vector_mas90 - proyeccion
                    # Normaliza el vector ortogonal
                    Porosityfield_dir2_array[n_elemento-1,:] = vector_ortogonal / np.linalg.norm(vector_ortogonal)
                n_elemento = n_elemento+1
                
                
                
# 	# Genera un vector aleatorio
# 	vector_aleatorio = np.random.rand(3)
# 	proyecciones = np.dot(Porosityfield_dir1_array, vector_aleatorio)[:, np.newaxis] * Porosityfield_dir1_array
# 	vector_ortogonal = vector_aleatorio - proyecciones
# 	# Normaliza el vector ortogonal
# 	Porosityfield_dir2_array = vector_ortogonal / np.linalg.norm(vector_ortogonal)
    Porosityfield_dir3_array = np.cross(Porosityfield_dir1_array,Porosityfield_dir2_array)

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
    for i in range(len(matriz_4d[:,0,0,0])):
        print(f"6 LOOP {i} out of matriz_4d {(len(matriz_4d[:, 0, 0]))}")
        for j in range(len(matriz_4d[0,:,0,0])):
            for k in range(len(matriz_4d[0,0,:,0])):
                coor_x = np.format_float_scientific(matriz_4d[i, j, k, 0],precision=6)
                coor_y = np.format_float_scientific(matriz_4d[i, j, k, 1],precision=6)
                coor_z = np.format_float_scientific(matriz_4d[i, j, k, 2],precision=6)
                gx.write(f"\n     {n_nodo}   {coor_x}  {coor_y}  {coor_z}   ")
                n_nodo = n_nodo+1

    # Alya geo file (End Section coordinates)
    gx.write("\nEND_COORDINATES")
    # Alya geo file (End file)
    gx.close()
    
    return Elementsetmaterials, numero_elemento, posicion_n_nodo, Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array