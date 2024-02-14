#####################################################################
#####################################################################
#####################################################################
#####################################################################

#########################  IMPORTANTE  ##############################

# Los puntos tienen que darse desde la esquina inferior izquierda (x negativo y
# z negativo) y en sentido contrario a las agujas del reloj.

# No está preparado para cualquier sección, solo secciones compuestas por
# rectángulos o rombos, como las secciones de los tows.

#####################################################################
#####################################################################
#####################################################################
#####################################################################


import math
import numpy as np
import sys
from stl import mesh

def generar_superficies_rectangulares(datos):
	# Crear una lista para almacenar los vértices de las superficies principales
	vertices_superficies = []
	
	# Crear una lista para almacenar los centros que definen la geometría
	centros_YarnX = []
	
	# Crear una lista para almacenar los planos
	planos_YarnX = []
	
	# Generar los vértices para las superficies principales
	for i in range(len(datos)):
		# Extraer las coordenadas X, Y, Z del punto
		x, y, z = datos[i, :3]
		
		# Obtener el ancho, alto y ángulo de giro para la superficie actual
		ancho, alto, angulo = datos[i, 3:]
		ancho = ancho/math.cos(math.radians(angulo))
		
		# Definir los vértices de la superficie centrada en el punto
		vertices = np.array([
			[x - ancho/2, y, z - alto/2],
			[x + ancho/2, y, z - alto/2],
			[x + ancho/2, y, z + alto/2],
			[x - ancho/2, y, z + alto/2]
		])
		
		# Obtener el punto central de la superficie
		centro = np.array([x, y, z])
        
        ####
        # Obtener el punto central de la superficie anterior (o la posterior si es la primera sup)
		if i != 0:
			xa, ya, za = datos[i-1, :3]
			centro_anterior = np.array([xa, ya, za])
			centro_actual = centro
		else:
			xa, ya, za = datos[i+1, :3]
			centro_anterior = centro
			centro_actual = np.array([xa, ya, za])
        # Rotación de los puntos en dirección de la directriz (solo en Z)
        # Definir dos vectores como arreglos de NumPy
		vector1 = np.array([0, 1, 0])
		vector1_xy = vector1[:2]
		vector2 = np.array([centro_actual[0]-centro_anterior[0], centro_actual[1]-centro_anterior[1], centro_actual[2]-centro_anterior[2]])
		vector2_xy = vector2[:2]

		# Calcular el ángulo en el plano XY
		cos_theta = np.dot(vector1_xy, vector2_xy) / (np.linalg.norm(vector1_xy) * np.linalg.norm(vector2_xy))

		# Convertir el ángulo a grados
		angulo_grados = np.degrees(np.arccos(cos_theta))
        
        # Rotar
		angulo_rad = math.radians(angulo_grados)
		rotation_matrix1 = np.array([
			[math.cos(angulo_rad), -math.sin(angulo_rad), 0],
			[math.sin(angulo_rad), math.cos(angulo_rad), 0],
			[0, 0, 1]
		])
		
		vertices = np.dot(vertices - centro, rotation_matrix1) + centro
        ####

        ####		
		# Realizar la rotación alrededor del eje Z en relación con el centro
		angulo_rad = math.radians(angulo)
		rotation_matrix = np.array([
			[math.cos(angulo_rad), -math.sin(angulo_rad), 0],
			[math.sin(angulo_rad), math.cos(angulo_rad), 0],
			[0, 0, 1]
		])
		vertices = np.dot(vertices - centro, rotation_matrix) + centro
		####
        
		# Agregar los vértices a la lista de superficies
		vertices_superficies.append(vertices)
		
		# Agregar los centros a la lista de centros de esta geoemtría
		centros_YarnX.append(centro)
		
		# Calcular y agregar los planos a la lista
		vector1 = np.array([vertices[1][0]-vertices[0][0], vertices[1][1]-vertices[0][1], vertices[1][2]-vertices[0][2]])
		vector2 = np.array([vertices[2][0]-vertices[0][0], vertices[2][1]-vertices[0][1], vertices[2][2]-vertices[0][2]])
		vector_normal = np.cross(vector2, vector1)
		vector_normal = vector_normal / np.linalg.norm(vector_normal)
		
		
		A, B, _ = vector_normal
		C = 0
		D = -A * vertices[0][0] - B * vertices[0][1] - C * vertices[0][2]
		planos_YarnX.append([A,B,C,D])
	
	# Crear una lista para almacenar todas las superficies (principales y laterales)
	superficies_totales = []
	
	# Agregar las superficies principales a la lista
	for i in range(len(vertices_superficies)):
		# Obtener los vértices de la superficie principal
		vertices_sup = vertices_superficies[i]
		
		# Definir los triángulos de la superficie
		caras = np.array([
			[0, 1, 2],
			[0, 2, 3]
		])
		
		# Crear la superficie utilizando los vértices y las caras
		superficie_principal = mesh.Mesh(np.zeros(caras.shape[0], dtype=mesh.Mesh.dtype))
		for j, cara in enumerate(caras):
			for k in range(3):
				superficie_principal.vectors[j][k] = vertices_sup[cara[k]]
		
		# Agregar la superficie principal a la lista
		superficies_totales.append(superficie_principal)
	
	# Crear una lista para almacenar las superficies laterales
	superficies_laterales = []
	
	superficies_laterales.append(superficies_totales[0])
	
	# Generar las superficies laterales
	for i in range(len(datos) - 1):
		# Definir los vértices de las superficies laterales
		vertices_s1 = vertices_superficies[i]
		vertices_s2 = vertices_superficies[i+1]
		
		# Unir las superficies laterales
		for j in range(4):
			lado1 = vertices_s1[j]
			lado2 = vertices_s2[j]
			
			superficie_lateral = mesh.Mesh(np.zeros(2, dtype=mesh.Mesh.dtype))
			superficie_lateral.vectors[0] = [lado1, lado2, vertices_s2[(j+1)%4]]
			superficie_lateral.vectors[1] = [lado1, vertices_s2[(j+1)%4], vertices_s1[(j+1)%4]]
			
			# Agregar la superficie lateral a la lista
			superficies_laterales.append(superficie_lateral)
	
	superficies_laterales.append(superficies_totales[-1])
	
	# Combinar todas las superficies (laterales) en un único objeto STL
	combined = mesh.Mesh(np.concatenate([s.data for s in superficies_laterales]))
    
	return combined, planos_YarnX, centros_YarnX


def generar_superficies_puntos(datos):
	# Crear una lista para almacenar los vértices de las superficies principales
	vertices_superficies = []
	
	# Crear una lista para almacenar los centros que definen la geometría
	centros_YarnX = []
	
	# Crear una lista para almacenar los planos
	planos_YarnX = []
	
	# Generar los vértices para las superficies principales
	for i in range(len(datos)):
		# Extraer las coordenadas X, Y, Z del punto
		x, y, z = datos[i, :3]
		
		# Obtener los n puntos que definen la sección
		puntos_seccion = datos[i, 3:]
		
		# Definir los vértices de la superficie centrada en el punto
		vertices = []
		for j in range(0, int((len(datos[i])-3)), 3):
			punto_x, punto_y, punto_z = puntos_seccion[j:j+3]
			vertices.append([x + punto_x, y + punto_y, z + punto_z])
		
		vertices = np.array(vertices)
		
		# Obtener el punto central de la superficie
		centro = np.array([x, y, z])
        
        ####
        # Obtener el punto central de la superficie anterior (o la posterior si es la primera sup)
		if i != 0:
			xa, ya, za = datos[i-1, :3]
			centro_anterior = np.array([xa, ya, za])
			centro_actual = centro
		else:
			xa, ya, za = datos[i+1, :3]
			centro_anterior = centro
			centro_actual = np.array([xa, ya, za])
        # Rotación de los puntos en dirección de la directriz (solo en Z)
        # Definir dos vectores como arreglos de NumPy
		vector1 = np.array([0, 1, 0])
		vector1_xy = vector1[:2]
		vector2 = np.array([centro_actual[0]-centro_anterior[0], centro_actual[1]-centro_anterior[1], centro_actual[2]-centro_anterior[2]])
		vector2_xy = vector2[:2]

		# Calcular el ángulo en el plano XY
		cos_theta = np.dot(vector1_xy, vector2_xy) / (np.linalg.norm(vector1_xy) * np.linalg.norm(vector2_xy))

		# Convertir el ángulo a grados
		angulo_grados = np.degrees(np.arccos(cos_theta))
        
        # Rotar
		angulo_rad = math.radians(angulo_grados)
		rotation_matrix1 = np.array([
			[math.cos(angulo_rad), -math.sin(angulo_rad), 0],
			[math.sin(angulo_rad), math.cos(angulo_rad), 0],
			[0, 0, 1]
		])
		
		vertices = np.dot(vertices - centro, rotation_matrix1) + centro
        ####

	
		# Agregar los vértices a la lista de superficies
		vertices_superficies.append(vertices)
		
		# Agregar los centros a la lista de centros de esta geoemtría
		centros_YarnX.append(centro)
		
		# Calcular y agregar los planos a la lista
		vector1 = np.array([vertices[1][0]-vertices[0][0], vertices[1][1]-vertices[0][1], vertices[1][2]-vertices[0][2]])
		vector2 = np.array([vertices[2][0]-vertices[0][0], vertices[2][1]-vertices[0][1], vertices[2][2]-vertices[0][2]])
		vector_normal = np.cross(vector2, vector1)
		vector_normal = vector_normal / np.linalg.norm(vector_normal)
		
		
		A, B, _ = vector_normal
		C = 0
		D = -A * vertices[0][0] - B * vertices[0][1] - C * vertices[0][2]
		planos_YarnX.append([A,B,C,D])
	
	# Crear una lista para almacenar todas las superficies (principales y laterales)
	superficies_totales = []
	
	# Agregar las superficies principales a la lista
	for i in range(len(vertices_superficies)):
		# Obtener los vértices de la superficie principal
		vertices_sup = vertices_superficies[i]
		
		# Definir los triángulos de la superficie
		if int(len(puntos_seccion)/3) == 4:
			caras = np.array([
				[0, 1, 2],
				[0, 2, 3]
			])
		elif int(len(puntos_seccion)/3) == 6:
			caras = np.array([
				[0, 1, 4],
				[0, 4, 5],
				[1, 2, 3],
				[1, 3, 4]
			])
		elif int(len(puntos_seccion)/3) == 8:
			caras = np.array([
				[0, 1, 6],
				[0, 6, 7],
				[1, 2, 5],
				[1, 5, 6],
				[2, 3, 4],
				[2, 4, 5]
			])
		elif int(len(puntos_seccion)/3) == 12:
			caras = np.array([
				[0, 1, 10],
				[0, 10, 11],
				[1, 2, 9],
				[1, 9, 10],
				[2, 3, 8],
				[2, 8, 9],
				[3, 4, 7],
				[3, 7, 8],
				[4, 5, 6],
				[4, 6, 7]
			])
		else:
			print("Error. La seccion no tiene 4, 6, 8 o 12 puntos")
			sys.exit()  # Termina la ejecución del programa
		
		# Crear la superficie utilizando los vértices y las caras
		superficie_principal = mesh.Mesh(np.zeros(caras.shape[0], dtype=mesh.Mesh.dtype))
		for j, cara in enumerate(caras):
			for k in range(3):
				superficie_principal.vectors[j][k] = vertices_sup[cara[k]]
		
		# Agregar la superficie principal a la lista
		superficies_totales.append(superficie_principal)
	
	# Crear una lista para almacenar las superficies laterales
	superficies_laterales = []
	
	superficies_laterales.append(superficies_totales[0])
	
	# Generar las superficies laterales
	for i in range(len(datos) - 1):
		vertices_s1 = vertices_superficies[i]
		vertices_s2 = vertices_superficies[i+1]
		
		# Unir las superficies laterales
		for j in range(int((len(datos[i])-3)/3)):
			lado1 = vertices_s1[j]
			lado2 = vertices_s2[j]
			
			superficie_lateral = mesh.Mesh(np.zeros(2, dtype=mesh.Mesh.dtype))
			superficie_lateral.vectors[0] = [lado1, lado2, vertices_s2[(j+1)%int((len(datos[i])-3)/3)]]
			superficie_lateral.vectors[1] = [lado1, vertices_s2[(j+1)%int((len(datos[i])-3)/3)], vertices_s1[(j+1)%int((len(datos[i])-3)/3)]]
			
			# Agregar la superficie lateral a la lista
			superficies_laterales.append(superficie_lateral)
	
	superficies_laterales.append(superficies_totales[-1])
	
	# Combinar todas las superficies (laterales) en un único objeto STL
	combined = mesh.Mesh(np.concatenate([s.data for s in superficies_laterales]))
    
    
	return combined, planos_YarnX, centros_YarnX

