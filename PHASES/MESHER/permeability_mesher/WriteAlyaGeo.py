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
    return vector - np.dot(vector, normal[:, np.newaxis]) * normal / np.linalg.norm(normal)**2

def calcular_angulo_entre_vectores(v1, v2):
    """
    Calcula el ángulo entre dos vectores.
    
    Parámetros:
    v1: np.array - Primer vector.
    v2: np.array - Segundo vector.
    
    Retorna:
    float - Ángulo en radianes entre los dos vectores.
    """
    with np.errstate(invalid='ignore'):  # Ignorar los warnings de invalid value encountered in divide
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1, axis=1) * np.linalg.norm(v2))
    angulo = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    return angulo

def writeAlyaGeo(outputMeshPath, caseName, dimXc, dimYc, dimZc, matriz_4d, matriz_4dc, matriz_3dc_inout, matriz_3dc_oris, angulos_tows, n_elementos_capa, matriz_3dc_FVF):
# Alya geo file
	lines = []
	#
	# Headers
	#
	# Alya geo file  (Section Nodes per element)
    #Dimensiones
	n_i = len(matriz_4d[:,0,0,0])
	n_j = len(matriz_4d[0,:,0,0])
	n_k = len(matriz_4d[0,0,:,0])
    
	lines.append("NODES_PER_ELEMENT")
	n_elems = dimXc*dimYc*dimZc
	for i in range(n_elems):
		lines.append("\n   "+str(int(i)+1)+" "+str(int(8)))  # Los modelos siempre van a ser hexaedros
	lines.append("\nEND_NODES_PER_ELEMENT")
    
    # Escribir todas las líneas al archivo de una vez
	with open(outputMeshPath + caseName + ".geo.dat","w", newline='\n') as gx:
		gx.writelines(lines)
	lines = []
    
	# Alya geo file
	lines.append("\nELEMENTS")
	n_nodo = 1
	posicion_n_nodo = np.zeros((n_i, n_j, n_k))
	for i in range(n_i):
		for j in range(n_j):
			for k in range(n_k):
				posicion_n_nodo[i,j,k]=n_nodo
				n_nodo = n_nodo + 1
    
    #Dimensiones
	nc_i = len(matriz_4dc[:,0,0,0])
	nc_j = len(matriz_4dc[0,:,0,0])
	nc_k = len(matriz_4dc[0,0,:,0])
	total_elements = nc_i * nc_j * nc_k 
    
	Elementsetmaterials = np.zeros((total_elements, int(3)))
	Porosityfield_dir1_array = np.zeros((total_elements, int(3)))
	Porosityfield_dir2_array = np.zeros((total_elements, int(3)))
	element_node_conectivity = np.zeros((total_elements, int(9)), dtype=int)
	numero_elemento = np.zeros((nc_i, nc_j, nc_k), dtype=int)
	
	# Índices para elementos
	indices = np.arange(1, total_elements + 1).reshape(nc_i, nc_j, nc_k)

	# Generar conectividad de nodos en un solo paso
	i, j, k = np.indices((nc_i, nc_j, nc_k))
	element_node_conectivity[:, 0] = indices.flatten()
	element_node_conectivity[:, 1] = posicion_n_nodo[i, j, k].flatten()
	element_node_conectivity[:, 2] = posicion_n_nodo[i+1, j, k].flatten()
	element_node_conectivity[:, 3] = posicion_n_nodo[i+1, j+1, k].flatten()
	element_node_conectivity[:, 4] = posicion_n_nodo[i, j+1, k].flatten()
	element_node_conectivity[:, 5] = posicion_n_nodo[i, j, k+1].flatten()
	element_node_conectivity[:, 6] = posicion_n_nodo[i+1, j, k+1].flatten()
	element_node_conectivity[:, 7] = posicion_n_nodo[i+1, j+1, k+1].flatten()
	element_node_conectivity[:, 8] = posicion_n_nodo[i, j+1, k+1].flatten()
    
	for i in range(len(element_node_conectivity)):
		lines.append(f'\n  {element_node_conectivity[i,0]} {element_node_conectivity[i,1]} {element_node_conectivity[i,2]} {element_node_conectivity[i,3]} {element_node_conectivity[i,4]} {element_node_conectivity[i,5]} {element_node_conectivity[i,6]} {element_node_conectivity[i,7]} {element_node_conectivity[i,8]}')
	del element_node_conectivity

    # Escribir todas las líneas al archivo de una vez
	with open(outputMeshPath + caseName + ".geo.dat","a", newline='\n') as gx:
		gx.writelines(lines)
	lines = []

	# Asignar FVF y materiales
	FVF = matriz_3dc_FVF.flatten()
	inout = matriz_3dc_inout.flatten()
	element_ids = np.arange(1, total_elements + 1)

	Elementsetmaterials[:, 0] = element_ids
	Elementsetmaterials[inout != 0, 1] = 2
	Elementsetmaterials[inout != 0, 2] = FVF[inout != 0]

	if np.any((inout == 0) & (FVF != 0)):
	    print('#########################')
	    print('NO COINCIDE FVF CON MATERIAL')
	    print('VER WriteAlyaGeo')
	    print('#########################')

	numero_elemento = indices

	# Asignar Porosityfield_dir1_array
	Porosityfield_dir1_array = matriz_3dc_oris[:, :, :, :3].reshape(total_elements, 3)

	# Calcular Porosityfield_dir2_array y ángulos
	u3 = np.array([0, 0, 1])
	dir_orientacion_0 = np.array([0, 1, 0])


	dir0_proyectado = proyectar_en_plano(dir_orientacion_0, u3)
	
	# Calcular ángulos
	angulo = np.degrees(calcular_angulo_entre_vectores(proyectar_en_plano(Porosityfield_dir1_array, u3), dir0_proyectado))
	
	# Vector ortogonal
	angulo = angulo + 90
	vector_mas90 = np.column_stack((np.cos(np.deg2rad(angulo)), np.sin(np.deg2rad(angulo)), np.zeros_like(angulo)))
	del angulo
	
	Porosityfield_dir2_array = (vector_mas90 - np.einsum('ij,ij->i', vector_mas90, Porosityfield_dir1_array)[:, np.newaxis] * Porosityfield_dir1_array) \
		/ np.linalg.norm(vector_mas90 - np.einsum('ij,ij->i', vector_mas90, Porosityfield_dir1_array)[:, np.newaxis] * Porosityfield_dir1_array, axis=1)[:, None]
	del vector_mas90                
    
    
	Porosityfield_dir3_array = np.cross(Porosityfield_dir1_array,Porosityfield_dir2_array)
	
	# Alya geo file (End Section elements)
	lines.append("\nEND_ELEMENTS")
	
	
	# Alya geo file (Section coordinates)
	lines.append("\nCOORDINATES")
	n_nodo = 1
	for i in range(n_i):
		for j in range(n_j):
			for k in range(n_k):
				coor_x = np.format_float_scientific(matriz_4d[i, j, k, 0],precision=6)
				coor_y = np.format_float_scientific(matriz_4d[i, j, k, 1],precision=6)
				coor_z = np.format_float_scientific(matriz_4d[i, j, k, 2],precision=6)
				lines.append(f"\n     {n_nodo}   {coor_x}  {coor_y}  {coor_z}   ")
				n_nodo = n_nodo+1
	
	# Alya geo file (End Section coordinates)    
	lines.append("\nEND_COORDINATES")

    
    # Escribir todas las líneas al archivo de una vez
	with open(outputMeshPath + caseName + ".geo.dat","a", newline='\n') as gx:
		gx.writelines(lines)
   
    
	return Elementsetmaterials, numero_elemento, posicion_n_nodo, Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array