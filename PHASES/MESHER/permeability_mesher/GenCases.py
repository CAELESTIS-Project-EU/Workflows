# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 11:15:16 2023

@author: cmagdalena
"""

import math
import numpy as np

def NoFallos(anchura, h_capa, L_pro, angulos_tows, n_capas, n_tows45, n_elementos_gap, n_elementos_towsingap, n_elementos_capa, factor_desplazamiento):
	for angulo in angulos_tows:
		if angulo==0 or angulo==90:
			angulo_dist_0_90 = 90.0
		else:
			angulo_dist_0_90 = angulo
			break 
	Ldom = n_tows45*(anchura+L_pro)/math.sin(math.radians(angulo_dist_0_90))
	seed_XY = L_pro/n_elementos_gap
	if L_pro==0:
		seed_XY = anchura/n_elementos_towsingap
	n_nodos = round(Ldom/seed_XY +1)  		# Número de puntos (nodos) equidistantes en X e Y, incluyendo el inicial y final 
	n_espesor = n_elementos_capa*n_capas+1	# Número de puntos (nodos) equidistantes en el espesor (Z), incluyendo el inicial y final
	L = math.sqrt(Ldom**2 + Ldom**2)
	N_tows = round(Ldom/anchura) + 1
	Tows_totales = n_capas*N_tows
	repeticion = (anchura + L_pro)
	x_ini = -Ldom
	y_ini = -Ldom/2.0
	
	desfase_array = np.empty(n_capas)
	mov_geometria_array = np.empty(n_capas)
	
	mover_geometria = -repeticion*(1/10)
	mover_geometria90 = -repeticion*(1/10)
	Ldom_Real90 = Ldom - mover_geometria - anchura/2 - L_pro
	Ldom_Real90_desf = Ldom - mover_geometria - anchura/2 - anchura/2 - L_pro
	Posicion_relativa90 = Ldom_Real90%(anchura+L_pro)
	Posicion_relativa90_desf = Ldom_Real90_desf%(anchura+L_pro)
	if Posicion_relativa90>anchura or Posicion_relativa90_desf>anchura:
		mover_geometria90=-(L_pro*1.5 + repeticion*(1/10))
	
	Ldom_Real0 = Ldom - mover_geometria - anchura/2 - anchura/2 - L_pro
	Ldom_Real0_desf = Ldom - mover_geometria - anchura/2 - L_pro
	Posicion_relativa0 = Ldom_Real0%(anchura+L_pro)
	Posicion_relativa0_desf = Ldom_Real0_desf%(anchura+L_pro)
	if Posicion_relativa0>anchura:
		mover_geometria = -(L_pro*1.5 + repeticion*(1/10))
	
	z = h_capa
	datos_input = []
	x_ini_ang = -1.5*Ldom/2.0
	y_ini_ang = -1.5*Ldom/2.0
	anchura90 = Ldom + 2*seed_XY
	corrector_desf90 = (anchura90+L_pro)/(anchura+L_pro)

	angulo_anterior = angulos_tows[0]
	desf_ant = 0
	desf = 0
	contador_par = 0
	contador_impar = 1
	for capa in range(n_capas):
		if capa%2==0:
			desf =0
		else:
			desf = -(anchura + L_pro)/2
		sin_alph = math.sin(math.radians(angulos_tows[capa]))
		cos_alph = math.cos(math.radians(angulos_tows[capa]))
		if angulos_tows[capa]==0:
			for tow in range(N_tows):
				datos_ini_izd = np.array([-Ldom/2.0 + mover_geometria - desf + repeticion*tow, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, 0])
				datos_fin_izd = np.array([-Ldom/2.0 + mover_geometria - desf + repeticion*tow, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, 0])
				datos_input_tow = np.vstack((datos_ini_izd, datos_fin_izd))
				datos_input.append(datos_input_tow)
			mov_geometria_array[capa] = mover_geometria
		elif angulos_tows[capa]==90:
			for tow in range(N_tows):
				datos_ini = np.array([-Ldom/2.0 - seed_XY,  -Ldom/2.0 + mover_geometria90 - desf + repeticion*tow, z/2.0 + z*capa, anchura, h_capa, 0])
				datos_fin = np.array([Ldom/2.0 + seed_XY,  -Ldom/2.0 + mover_geometria90 - desf + repeticion*tow, z/2.0 + z*capa, anchura, h_capa, 0])
				datos_input_tow = np.vstack((datos_ini, datos_fin))
				datos_input.append(datos_input_tow)
			mov_geometria_array[capa] = mover_geometria90
		elif angulos_tows[capa]<90:
			contador_par = 0
			contador_impar = 1
			for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([0 - L*cos_alph, 0 - L*sin_alph + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, 0])
						datos_fin = np.array([0 + L*cos_alph, 0 + L*sin_alph + desf/cos_alph  + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, 0])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([0 - L*cos_alph, 0 - L*sin_alph + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, 0])
						datos_fin = np.array([0 + L*cos_alph, 0 + L*sin_alph + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, 0])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			mov_geometria_array[capa] = 0
		elif angulos_tows[capa]>90:
			contador_par = 0
			contador_impar = 1
			for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([0 + L*cos_alph, 0 + L*sin_alph + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, 0])
						datos_fin = np.array([0 - L*cos_alph, 0 - L*sin_alph + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, 0])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([0 + L*cos_alph, 0 + L*sin_alph + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, 0])
						datos_fin = np.array([0 - L*cos_alph, 0 - L*sin_alph + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, 0])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			mov_geometria_array[capa] = 0
		desfase_array[capa] = desf

	return datos_input, n_nodos, n_espesor, Ldom, desfase_array, mov_geometria_array

def Overlap(anchura, h_capa, L_pro, ol, ajus_ol, ol_izd, ol_drch, angulos_tows, n_capas, n_tows45, n_elementos_gap, n_elementos_towsingap, n_elementos_capa, factor_desplazamiento):
	angulos_seccion = [0, 0, 0, 0, 0, 0, 0] #Para NoFallos, todo 0
	for angulo in angulos_tows:
		if angulo==0 or angulo==90:
			angulo_dist_0_90 = 90.0
		else:
			angulo_dist_0_90 = angulo
			break 
	Ldom = n_tows45*(anchura+L_pro)/math.sin(math.radians(angulo_dist_0_90))
	seed_XY = L_pro/n_elementos_gap
	if L_pro==0:
		seed_XY = anchura/n_elementos_towsingap
	n_nodos = round(Ldom/seed_XY +1)  		# Número de puntos (nodos) equidistantes en X e Y, incluyendo el inicial y final 
	n_espesor = n_elementos_capa*n_capas+1	# Número de puntos (nodos) equidistantes en el espesor (Z), incluyendo el inicial y final
	L = math.sqrt(Ldom**2 + Ldom**2)
	N_tows = round(Ldom/anchura) + 1
	Tows_totales = n_capas*N_tows
	repeticion = (anchura + L_pro)
	x_ini = -Ldom
	y_ini = -Ldom/2.0
	
	desfase_array = np.empty(n_capas)
	mov_geometria_array = np.empty(n_capas)
	

	mover_geometria = -repeticion*(factor_desplazamiento)
	mover_geometria90 = -repeticion*(factor_desplazamiento)
	
	Ldom_Real90 = Ldom - mover_geometria90 - anchura/2 - L_pro
	Ldom_Real90_desf = Ldom + anchura/2 - mover_geometria90 - anchura/2 - L_pro
	Posicion_relativa90 = Ldom_Real90%(anchura+L_pro)
	Posicion_relativa90_desf = Ldom_Real90_desf%(anchura+L_pro)
	if Posicion_relativa90>anchura or Posicion_relativa90_desf>anchura:
		mover_geometria90=-(L_pro*1.5 + repeticion*(factor_desplazamiento))
	
	Ldom_Real0_izd = Ldom/2 - anchura + mover_geometria - L_pro - anchura/2
	Ldom_Real0_drch = Ldom/2 - anchura + mover_geometria + repeticion - anchura/2 - L_pro
	Ldom_Real0_izd_desf = Ldom/2 - anchura - anchura/2 + mover_geometria - L_pro - anchura/2
	Ldom_Real0_drch_desf = Ldom/2 - anchura - anchura/2 + mover_geometria + repeticion - anchura/2 - L_pro
	Posicion_relativa0_izd = Ldom_Real0_izd%(anchura+L_pro)
	Posicion_relativa0_drch = Ldom_Real0_drch%(anchura+L_pro)
	Posicion_relativa0_izd_desf = Ldom_Real0_izd_desf%(anchura+L_pro)
	Posicion_relativa0_drch_desf = Ldom_Real0_drch_desf%(anchura+L_pro)
	if Posicion_relativa0_izd>anchura or Posicion_relativa0_izd_desf>anchura or Posicion_relativa0_drch>anchura or Posicion_relativa0_drch_desf>anchura:
		mover_geometria=-(L_pro*1.5 + repeticion*(factor_desplazamiento))
	
	z = h_capa
	h_ol = h_capa*ajus_ol
	datos_input = []
	x_ini_ang = -1.5*Ldom/2.0
	y_ini_ang = -1.5*Ldom/2.0
	anchura90 = Ldom
	corrector_desf90 = (anchura90+L_pro)/(anchura+L_pro)

	angulo_anterior = angulos_tows[0]
	desf_ant = 0
	desf = 0
	contador_par = 0
	contador_impar = 1
	for capa in range(n_capas):
		if capa==0:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			desf = 0
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				datos_ini_izd = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_izd = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_izd, datos_fin_izd))
				datos_input.append(datos_input_tow)

				datos_ini_drch = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_drch = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_drch, datos_fin_drch))
				datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow== 0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion +  repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
						datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		if capa==1:
			mov_geometria_array[capa] = mover_geometria
			desf = -(anchura + L_pro)/2 + L_pro/2
			desfase_array[capa] = desf
			# punto1_izd
			x1_izd = -anchura/2
			y1_izd = 0
			z1_izd = -h_capa/2
			# punto2_izd
			x2_izd = anchura/2
			y2_izd = 0
			z2_izd = -h_capa/2
			# punto3_izd
			x3_izd = anchura/2
			y3_izd = 0
			z3_izd = h_capa/2 - (h_capa - h_ol)
			# punto4_izd
			x4_izd = anchura/2 - ol + L_pro 
			y4_izd = 0
			z4_izd = h_capa/2 - (h_capa - h_ol)
			# punto5_izd
			x5_izd = anchura/2 - ol + L_pro - ol_izd
			y5_izd = 0
			z5_izd = h_capa/2
			# punto6_izd
			x6_izd = -anchura/2
			y6_izd = 0
			z6_izd = h_capa/2
			datos_ini = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd])
			datos_fin = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd])
			datos_input_tow = np.vstack((datos_ini, datos_fin))
			datos_input.append(datos_input_tow)
			
			# punto1_drch
			x1_drch = -anchura/2
			y1_drch = 0
			z1_drch = h_capa/2 - (h_capa - h_ol)
			# punto2_drch
			x2_drch = -anchura/2 - L_pro + ol
			y2_drch = 0
			z2_drch = h_capa/2 - (h_capa - h_ol)
			# punto3_drch
			x3_drch = -anchura/2 - L_pro + ol_drch + ol
			y3_drch = 0
			z3_drch = -h_capa/2
			# punto4_drch
			x4_drch = anchura/2
			y4_drch = 0
			z4_drch = -h_capa/2
			# punto5_drch
			x5_drch = anchura/2
			y5_drch = 0
			z5_drch = h_capa/2
			# punto6_drch
			x6_drch = -anchura/2 - L_pro + ol_drch + ol
			y6_drch = 0
			z6_drch = h_capa/2
			# punto7_drch
			x7_drch = -anchura/2 - L_pro + ol
			y7_drch = 0
			z7_drch = h_capa/2  - (h_capa - h_ol) + h_ol
			# punto8_drch
			x8_drch = -anchura/2
			y8_drch = 0
			z8_drch = h_capa/2  - (h_capa - h_ol) + h_ol
			datos_ini = np.array([-ol -anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch, x7_drch, y7_drch, z7_drch, x8_drch, y8_drch, z8_drch])
			datos_fin = np.array([-ol -anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch, x7_drch, y7_drch, z7_drch, x8_drch, y8_drch, z8_drch])
			datos_input_tow = np.vstack((datos_ini, datos_fin))
			datos_input.append(datos_input_tow)

			contador_izd = 1
			contador_drch = 1
			for tow in range(N_tows):
				if tow==0 or tow%2==0:
					datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)
					contador_izd = contador_izd + 1
				else:
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)
					contador_drch = contador_drch + 1
		contador_par = 0
		contador_impar = 1
		if capa==2:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			tan_alph = math.tan(math.radians(angulos_tows[capa]))
			tan_beta = math.tan(math.radians(90 - angulos_tows[capa]))
			desf = 0
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				datos_ini_izd = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_izd = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_izd, datos_fin_izd))
				datos_input.append(datos_input_tow)

				# punto1
				x1 = -anchura/2
				y1 = 0
				z1 = -h_capa/2
				# punto2
				x2 = -ol - ol_izd
				y2 = 0
				z2 = -h_capa/2
				# punto3
				x3 = -ol
				y3 = 0
				z3 = -h_capa/2  - (h_capa - h_ol) + h_ol
				# punto4
				x4 = -L_pro
				y4 = 0
				z4 = -h_capa/2  - (h_capa - h_ol) + h_ol
				# punto5
				x5 = -L_pro + ol_drch
				y5 = 0
				z5 = -h_capa/2
				# punto6
				x6 = anchura/2
				y6 = 0
				z6 = -h_capa/2
				# punto7
				x7 = anchura/2 
				y7 = 0
				z7 = h_capa/2
				# punto8
				x8 = -L_pro + ol_drch
				y8 = 0
				z8 = h_capa/2
				# punto9
				x9 = -L_pro
				y9 = 0
				z9 = -h_capa/2  - (h_capa - h_ol) + 2*h_ol
				# punto10
				x10 = -ol
				y10 = 0
				z10 = -h_capa/2  - (h_capa - h_ol) + 2*h_ol
				# punto11
				x11 = -ol - ol_izd
				y11 = 0
				z11 = h_capa/2
				# punto12
				x12 = -anchura/2
				y12 = 0
				z12 = h_capa/2
				datos_ini_drch = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, x5, y5, z5, x6, y6, z6, x7, y7, z7, x8, y8, z8, x9, y9, z9, x10, y10, z10, x11, y11, z11, x12, y12, z12])
				datos_fin_drch = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, x5, y5, z5, x6, y6, z6, x7, y7, z7, x8, y8, z8, x9, y9, z9, x10, y10, z10, x11, y11, z11, x12, y12, z12])
				datos_input_tow = np.vstack((datos_ini_drch, datos_fin_drch))
				datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow== 0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
					datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_1 = np.array([-ol_izd - ol + L_pro + mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_2 = np.array([-ol + L_pro+ mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_3 = np.array([mover_geometria,  -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_4 = np.array([mover_geometria + ol_drch, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_1, datos_2, datos_3, datos_4, datos_fin))
					datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow==0 or tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		contador_par = 0
		contador_impar = 1
		if capa==3:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			tan_alph = math.tan(math.radians(angulos_tows[capa]))
			tan_beta = math.tan(math.radians(90 - angulos_tows[capa]))
			desf = -(anchura + L_pro)/2 + L_pro/2
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				# punto1_izd
				x1_izd = -anchura/2
				y1_izd = 0
				z1_izd = -h_capa/2
				# punto2_izd
				x2_izd = anchura/2 - ol - ol_izd + L_pro
				y2_izd = 0
				z2_izd = -h_capa/2
				# punto3_izd
				x3_izd = anchura/2 - ol + L_pro
				y3_izd = 0
				z3_izd = -h_capa/2  - 2*(h_capa - h_ol) + h_ol
				# punto4_izd
				x4_izd = anchura/2
				y4_izd = 0
				z4_izd = -h_capa/2  - 2*(h_capa - h_ol) + h_ol
				# punto5_izd
				x5_izd = anchura/2
				y5_izd = 0
				z5_izd = -h_capa/2  - 2*(h_capa - h_ol) + 2*h_ol
				# punto6_izd
				x6_izd = anchura/2 - ol + L_pro
				y6_izd = 0
				z6_izd = -h_capa/2  - 2*(h_capa - h_ol) + 2*h_ol
				# punto7_izd
				x7_izd = anchura/2 - ol - ol_izd + L_pro
				y7_izd = 0
				z7_izd = h_capa/2
				# punto8_izd
				x8_izd = -anchura/2
				y8_izd = 0
				z8_izd = h_capa/2
				datos_ini = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
				datos_fin = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
				datos_input_tow = np.vstack((datos_ini, datos_fin))
				datos_input.append(datos_input_tow)
				
				if L_pro<=ol_drch:
					beta = math.atan((3*h_ol - 2*h_capa)/ol_drch)
					# punto1_drch
					x1_drch = -anchura/2
					y1_drch = 0
					z1_drch = -h_capa/2 + (ol_drch - L_pro)*math.tan(beta)
					# punto2_drch
					x2_drch = -anchura/2 + ol_drch - L_pro
					y2_drch = 0
					z2_drch = -h_capa/2
					# punto3_drch
					x3_drch = anchura/2
					y3_drch = 0
					z3_drch = -h_capa/2
					# punto4_drch
					x4_drch = anchura/2
					y4_drch = 0
					z4_drch = h_capa/2
					# punto5_drch
					x5_drch = -anchura/2 + ol_drch - L_pro
					y5_drch = 0
					z5_drch = h_capa/2
					# punto6_drch
					x6_drch = -anchura/2
					y6_drch = 0
					z6_drch = -h_capa/2 + (ol_drch - L_pro)*math.tan(beta) + h_ol + ((L_pro)/ol_drch)*(h_capa - h_ol)
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom +seed_XY, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)
					
				else:
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom +seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow==0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
					datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_1 = np.array([-ol_izd - ol + L_pro + mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_2 = np.array([-ol + L_pro+ mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_3 = np.array([mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_4 = np.array([mover_geometria + ol_drch,  -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_1, datos_2, datos_3, datos_4, datos_fin))
					datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow==0 or tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		contador_par = 0
		contador_impar = 1
		if capa==4:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			tan_alph = math.tan(math.radians(angulos_tows[capa]))
			tan_beta = math.tan(math.radians(90 - angulos_tows[capa]))
			desf = 0
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				datos_ini_izd = np.array([-anchura - desf + mover_geometria - desf, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_izd = np.array([-anchura - desf + mover_geometria - desf, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_izd, datos_fin_izd))
				datos_input.append(datos_input_tow)

				# punto1
				x1 = -anchura/2
				y1 = 0
				z1 = -h_capa/2
				# punto2
				x2 = -ol - ol_izd 
				y2 = 0
				z2 = -h_capa/2
				# punto3
				x3 = -ol
				y3 = 0
				z3 = -h_capa/2  - 3*(h_capa - h_ol) + h_ol
				# punto4
				x4 = -L_pro
				y4 = 0
				z4 = -h_capa/2  - 3*(h_capa - h_ol) + h_ol
				# punto5
				x5 = -L_pro + ol_drch
				y5 = 0
				z5 = -h_capa/2
				# punto6
				x6 = anchura/2
				y6 = 0
				z6 = -h_capa/2
				# punto7
				x7 = anchura/2 
				y7 = 0
				z7 = h_capa/2
				# punto8
				x8 = -L_pro + ol_drch
				y8 = 0
				z8 = h_capa/2
				# punto9
				x9 = -L_pro
				y9 = 0
				z9 = -h_capa/2  - 3*(h_capa - h_ol) + 2*h_ol
				# punto10
				x10 = -ol
				y10 = 0
				z10 = -h_capa/2  - 3*(h_capa - h_ol) + 2*h_ol
				# punto11
				x11 = -ol - ol_izd
				y11 = 0
				z11 = h_capa/2
				# punto12
				x12 = -anchura/2
				y12 = 0
				z12 = h_capa/2
				datos_ini_drch = np.array([-anchura - desf + mover_geometria - desf + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, x5, y5, z5, x6, y6, z6, x7, y7, z7, x8, y8, z8, x9, y9, z9, x10, y10, z10, x11, y11, z11, x12, y12, z12])
				datos_fin_drch = np.array([-anchura - desf + mover_geometria - desf + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, x5, y5, z5, x6, y6, z6, x7, y7, z7, x8, y8, z8, x9, y9, z9, x10, y10, z10, x11, y11, z11, x12, y12, z12])
				datos_input_tow = np.vstack((datos_ini_drch, datos_fin_drch))
				datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow== 0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - desf - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - desf - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria - desf + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - desf + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
					datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_1 = np.array([-ol_izd - ol + L_pro + mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_2 = np.array([-ol + L_pro+ mover_geometria,  -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_3 = np.array([mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_4 = np.array([mover_geometria + ol_drch, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_1, datos_2, datos_3, datos_4, datos_fin))
					datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow==0 or tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria+ abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		contador_par = 0
		contador_impar = 1
		if capa==5:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			tan_alph = math.tan(math.radians(angulos_tows[capa]))
			tan_beta = math.tan(math.radians(90 - angulos_tows[capa]))
			desf = -(anchura + L_pro)/2 + L_pro/2
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				# punto1_izd
				x1_izd = -anchura/2
				y1_izd = 0
				z1_izd = -h_capa/2
				# punto2_izd
				x2_izd = anchura/2 - ol - ol_izd + L_pro
				y2_izd = 0
				z2_izd = -h_capa/2
				# punto3_izd
				x3_izd = anchura/2 - ol + L_pro
				y3_izd = 0
				z3_izd = -h_capa/2  - 4*(h_capa - h_ol) + h_ol
				# punto4_izd
				x4_izd = anchura/2
				y4_izd = 0
				z4_izd = -h_capa/2  - 4*(h_capa - h_ol) + h_ol
				# punto5_izd
				x5_izd = anchura/2
				y5_izd = 0
				z5_izd = -h_capa/2  - 4*(h_capa - h_ol) + 2*h_ol
				# punto6_izd
				x6_izd = anchura/2 - ol + L_pro
				y6_izd = 0
				z6_izd = -h_capa/2  - 4*(h_capa - h_ol) + 2*h_ol
				# punto7_izd
				x7_izd = anchura/2 - ol - ol_izd + L_pro
				y7_izd = 0
				z7_izd = h_capa/2
				# punto8_izd
				x8_izd = -anchura/2
				y8_izd = 0
				z8_izd = h_capa/2
				datos_ini = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
				datos_fin = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
				datos_input_tow = np.vstack((datos_ini, datos_fin))
				datos_input.append(datos_input_tow)

				if L_pro<=ol_drch:
					beta = math.atan((5*h_ol - 4*h_capa)/ol_drch)
					# punto1_drch
					x1_drch = -anchura/2
					y1_drch = 0
					z1_drch = -h_capa/2 + (ol_drch - L_pro)*math.tan(beta)
					# punto2_drch
					x2_drch = -anchura/2 + ol_drch - L_pro
					y2_drch = 0
					z2_drch = -h_capa/2
					# punto3_drch
					x3_drch = anchura/2
					y3_drch = 0
					z3_drch = -h_capa/2
					# punto4_drch
					x4_drch = anchura/2
					y4_drch = 0
					z4_drch = h_capa/2
					# punto5_drch
					x5_drch = -anchura/2 + ol_drch - L_pro
					y5_drch = 0
					z5_drch = h_capa/2
					# punto6_drch
					x6_drch = -anchura/2
					y6_drch = 0
					z6_drch = -h_capa/2 + (ol_drch - L_pro)*math.tan(beta) + h_ol + ((L_pro)/ol_drch)*(h_capa - h_ol)
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)

				else:
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom +seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)
				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow==0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
					datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_1 = np.array([-ol_izd - ol + L_pro + mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_2 = np.array([-ol + L_pro+ mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_3 = np.array([mover_geometria,  -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_4 = np.array([mover_geometria + ol_drch, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_1, datos_2, datos_3, datos_4, datos_fin))
					datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow==0 or tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		contador_par = 0 
		contador_impar = 0
		if capa==6:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			desf = 0
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				datos_ini_izd = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_izd = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_izd, datos_fin_izd))
				datos_input.append(datos_input_tow)

				datos_ini_drch = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_drch = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_drch, datos_fin_drch))
				datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow== 0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion +  repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
						datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
	               
	return datos_input, n_nodos, n_espesor, Ldom, desfase_array, mov_geometria_array

def Gap(anchura, h_capa, L_pro, ol, ajus_ol, ol_izd, ol_drch, angulos_tows, n_capas, n_tows45, n_elementos_gap, n_elementos_towsingap, n_elementos_capa, factor_desplazamiento):
	angulos_seccion = [0, 0, 0, 0, 0, 0, 0] #Para NoFallos, todo 0
	for angulo in angulos_tows:
		if angulo==0 or angulo==90:
			angulo_dist_0_90 = 90.0
		else:
			angulo_dist_0_90 = angulo
			break 
	Ldom = n_tows45*(anchura+L_pro)/math.sin(math.radians(angulo_dist_0_90))
	seed_XY = L_pro/n_elementos_gap
	if L_pro==0:
		seed_XY = anchura/n_elementos_towsingap
	n_nodos = round(Ldom/seed_XY +1)  		# Número de puntos (nodos) equidistantes en X e Y, incluyendo el inicial y final 
	n_espesor = n_elementos_capa*n_capas+1	# Número de puntos (nodos) equidistantes en el espesor (Z), incluyendo el inicial y final
	L = math.sqrt(Ldom**2 + Ldom**2)
	N_tows = round(Ldom/anchura) + 1
	Tows_totales = n_capas*N_tows
	repeticion = (anchura + L_pro)
	x_ini = -Ldom
	y_ini = -Ldom/2.0
	
	desfase_array = np.empty(n_capas)
	mov_geometria_array = np.empty(n_capas)
	
	mover_geometria = -repeticion*(factor_desplazamiento)
	mover_geometria90 = -repeticion*(factor_desplazamiento)
	
	Ldom_Real90 = Ldom - mover_geometria90 - anchura/2 - L_pro
	Ldom_Real90_desf = Ldom + anchura/2 - mover_geometria90 - anchura/2 - L_pro
	Posicion_relativa90 = Ldom_Real90%(anchura+L_pro)
	Posicion_relativa90_desf = Ldom_Real90_desf%(anchura+L_pro)
	if Posicion_relativa90>anchura or Posicion_relativa90_desf>anchura:
		mover_geometria90=-(L_pro*1.5 + repeticion*(factor_desplazamiento))
	
	Ldom_Real0_izd = Ldom/2 - anchura + mover_geometria - L_pro - anchura/2
	Ldom_Real0_drch = Ldom/2 - anchura + mover_geometria + repeticion - anchura/2 - L_pro
	Ldom_Real0_izd_desf = Ldom/2 - anchura - anchura/2 + mover_geometria - L_pro - anchura/2
	Ldom_Real0_drch_desf = Ldom/2 - anchura - anchura/2 + mover_geometria + repeticion - anchura/2 - L_pro
	Posicion_relativa0_izd = Ldom_Real0_izd%(anchura+L_pro)
	Posicion_relativa0_drch = Ldom_Real0_drch%(anchura+L_pro)
	Posicion_relativa0_izd_desf = Ldom_Real0_izd_desf%(anchura+L_pro)
	Posicion_relativa0_drch_desf = Ldom_Real0_drch_desf%(anchura+L_pro)
	if Posicion_relativa0_izd>anchura or Posicion_relativa0_izd_desf>anchura or Posicion_relativa0_drch>anchura or Posicion_relativa0_drch_desf>anchura:
		mover_geometria=-(L_pro*1.5 + repeticion*(factor_desplazamiento))
	
	z = h_capa
	h_ol = h_capa*ajus_ol
	datos_input = []
	x_ini_ang = -1.5*Ldom/2.0
	y_ini_ang = -1.5*Ldom/2.0
	anchura90 = Ldom
	corrector_desf90 = (anchura90+L_pro)/(anchura+L_pro)

	angulo_anterior = angulos_tows[0]
	desf_ant = 0
	desf = 0
	contador_par = 0
	contador_impar = 1
	for capa in range(n_capas):
		if capa==0:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			desf = 0
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				datos_ini_izd = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_izd = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_izd, datos_fin_izd))
				datos_input.append(datos_input_tow)

				datos_ini_drch = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_drch = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_drch, datos_fin_drch))
				datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow== 0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion +  repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
						datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		if capa==1:
			desf = -(anchura + L_pro)/2 + L_pro/2
			desfase_array[capa] = desf
			mov_geometria_array[capa] = mover_geometria
			# punto1_izd
			x1_izd = -anchura/2
			y1_izd = 0
			z1_izd = -h_capa/2
			# punto2_izd
			x2_izd = anchura/2 - ol - ol_izd + L_pro
			y2_izd = 0
			z2_izd = -h_capa/2
			# punto3_izd
			x3_izd = anchura/2 - ol + L_pro
			y3_izd = 0
			z3_izd = h_capa/2 - (h_capa - h_ol)
			# punto4_izd
			x4_izd = anchura/2
			y4_izd = 0
			z4_izd = h_capa/2 - (h_capa - h_ol)
			# punto5_izd
			x5_izd = anchura/2
			y5_izd = 0
			z5_izd = h_capa/2 - (h_capa - h_ol) + h_ol
			# punto6_izd
			x6_izd = anchura/2 - ol + L_pro
			y6_izd = 0
			z6_izd = h_capa/2 - (h_capa - h_ol) + h_ol
			# punto7_izd
			x7_izd = anchura/2 - ol - ol_izd + L_pro
			y7_izd = 0
			z7_izd = h_capa/2
			# punto8_izd
			x8_izd = -anchura/2
			y8_izd = 0
			z8_izd = h_capa/2
			datos_ini = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
			datos_fin = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
			datos_input_tow = np.vstack((datos_ini, datos_fin))
			datos_input.append(datos_input_tow)

			# punto1_drch
			x1_drch = -anchura/2
			y1_drch = 0
			z1_drch = -h_capa/2
			# punto2_drch
			x2_drch = anchura/2
			y2_drch = 0
			z2_drch = -h_capa/2
			# punto3_drch
			x3_drch = anchura/2
			y3_drch = 0
			z3_drch = h_capa/2
			# punto4_drch
			x4_drch = -anchura/2 - L_pro + ol_drch + ol
			y4_drch = 0
			z4_drch = h_capa/2
			# punto5_drch
			x5_drch = -anchura/2 - L_pro + ol
			y5_drch = 0
			z5_drch = h_capa/2 - (h_capa - h_ol)
			# punto6_drch
			x6_drch = -anchura/2
			y6_drch = 0
			z6_drch = h_capa/2 - (h_capa - h_ol)
			datos_ini = np.array([-ol -anchura - desf + mover_geometria +  repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
			datos_fin = np.array([-ol -anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
			datos_input_tow = np.vstack((datos_ini, datos_fin))
			datos_input.append(datos_input_tow)
			
			contador_izd = 1
			contador_drch = 1
			for tow in range(N_tows):
				if tow==0 or tow%2==0:
					datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)
					contador_izd = contador_izd + 1
				else:
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)
					contador_drch = contador_drch + 1
		contador_par = 0
		contador_impar = 1
		if capa==2:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			tan_alph = math.tan(math.radians(angulos_tows[capa]))
			tan_beta = math.tan(math.radians(90 - angulos_tows[capa]))
			desf = 0
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				datos_ini_izd = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_izd = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_izd, datos_fin_izd))
				datos_input.append(datos_input_tow)

				# punto1
				x1 = -anchura/2
				y1 = 0
				z1 = -h_capa/2
				# punto2
				x2 = -ol - ol_izd
				y2 = 0
				z2 = -h_capa/2
				# punto3
				x3 = -ol
				y3 = 0
				z3 = -h_capa/2  - (h_capa - h_ol) + h_ol
				# punto4
				x4 = -L_pro
				y4 = 0
				z4 = -h_capa/2  - (h_capa - h_ol) + h_ol
				# punto5
				x5 = -L_pro + ol_drch
				y5 = 0
				z5 = -h_capa/2
				# punto6
				x6 = anchura/2
				y6 = 0
				z6 = -h_capa/2
				# punto7
				x7 = anchura/2 
				y7 = 0
				z7 = h_capa/2
				# punto8
				x8 = -L_pro + ol_drch
				y8 = 0
				z8 = h_capa/2
				# punto9
				x9 = -L_pro
				y9 = 0
				z9 = -h_capa/2  - (h_capa - h_ol) + 2*h_ol
				# punto10
				x10 = -ol
				y10 = 0
				z10 = -h_capa/2  - (h_capa - h_ol) + 2*h_ol
				# punto11
				x11 = -ol - ol_izd
				y11 = 0
				z11 = h_capa/2
				# punto12
				x12 = -anchura/2
				y12 = 0
				z12 = h_capa/2
				datos_ini_drch = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, x5, y5, z5, x6, y6, z6, x7, y7, z7, x8, y8, z8, x9, y9, z9, x10, y10, z10, x11, y11, z11, x12, y12, z12])
				datos_fin_drch = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, x5, y5, z5, x6, y6, z6, x7, y7, z7, x8, y8, z8, x9, y9, z9, x10, y10, z10, x11, y11, z11, x12, y12, z12])
				datos_input_tow = np.vstack((datos_ini_drch, datos_fin_drch))
				datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow== 0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
					datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_1 = np.array([-ol_izd - ol + L_pro + mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_2 = np.array([-ol + L_pro+ mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_3 = np.array([mover_geometria,  -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_4 = np.array([mover_geometria + ol_drch, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_1, datos_2, datos_3, datos_4, datos_fin))
					datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow==0 or tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 1.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		contador_par = 0
		contador_impar = 1
		if capa==3:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			tan_alph = math.tan(math.radians(angulos_tows[capa]))
			tan_beta = math.tan(math.radians(90 - angulos_tows[capa]))
			desf = -(anchura + L_pro)/2 + L_pro/2
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				# punto1_izd
				x1_izd = -anchura/2
				y1_izd = 0
				z1_izd = -h_capa/2
				# punto2_izd
				x2_izd = anchura/2 - ol - ol_izd + L_pro
				y2_izd = 0
				z2_izd = -h_capa/2
				# punto3_izd
				x3_izd = anchura/2 - ol + L_pro
				y3_izd = 0
				z3_izd = -h_capa/2  - 2*(h_capa - h_ol) + h_ol
				# punto4_izd
				x4_izd = anchura/2
				y4_izd = 0
				z4_izd = -h_capa/2  - 2*(h_capa - h_ol) + h_ol
				# punto5_izd
				x5_izd = anchura/2
				y5_izd = 0
				z5_izd = -h_capa/2  - 2*(h_capa - h_ol) + 2*h_ol
				# punto6_izd
				x6_izd = anchura/2 - ol + L_pro
				y6_izd = 0
				z6_izd = -h_capa/2  - 2*(h_capa - h_ol) + 2*h_ol
				# punto7_izd
				x7_izd = anchura/2 - ol - ol_izd + L_pro
				y7_izd = 0
				z7_izd = h_capa/2
				# punto8_izd
				x8_izd = -anchura/2
				y8_izd = 0
				z8_izd = h_capa/2
				datos_ini = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
				datos_fin = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
				datos_input_tow = np.vstack((datos_ini, datos_fin))
				datos_input.append(datos_input_tow)

				if L_pro<=ol_drch:
					beta = math.atan((3*h_ol - 2*h_capa)/ol_drch)
					# punto1_drch
					x1_drch = -anchura/2
					y1_drch = 0
					z1_drch = -h_capa/2 + (ol_drch - L_pro)*math.tan(beta)
					# punto2_drch
					x2_drch = -anchura/2 + ol_drch - L_pro
					y2_drch = 0
					z2_drch = -h_capa/2
					# punto3_drch
					x3_drch = anchura/2
					y3_drch = 0
					z3_drch = -h_capa/2
					# punto4_drch
					x4_drch = anchura/2
					y4_drch = 0
					z4_drch = h_capa/2
					# punto5_drch
					x5_drch = -anchura/2 + ol_drch - L_pro
					y5_drch = 0
					z5_drch = h_capa/2
					# punto6_drch
					x6_drch = -anchura/2
					y6_drch = 0
					z6_drch = -h_capa/2 + (ol_drch - L_pro)*math.tan(beta) + h_ol + ((L_pro)/ol_drch)*(h_capa - h_ol)
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom +seed_XY, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)

				else:
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom +seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow==0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
					datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_1 = np.array([-ol_izd - ol + L_pro + mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_2 = np.array([-ol + L_pro+ mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_3 = np.array([mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_4 = np.array([mover_geometria + ol_drch,  -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_1, datos_2, datos_3, datos_4, datos_fin))
					datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow==0 or tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 2.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		contador_par = 0
		contador_impar = 1
		if capa==4:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			tan_alph = math.tan(math.radians(angulos_tows[capa]))
			tan_beta = math.tan(math.radians(90 - angulos_tows[capa]))
			desf = 0
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				datos_ini_izd = np.array([-anchura - desf + mover_geometria - desf, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_izd = np.array([-anchura - desf + mover_geometria - desf, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_izd, datos_fin_izd))
				datos_input.append(datos_input_tow)

				# punto1
				x1 = -anchura/2
				y1 = 0
				z1 = -h_capa/2
				# punto2
				x2 = -ol - ol_izd 
				y2 = 0
				z2 = -h_capa/2
				# punto3
				x3 = -ol
				y3 = 0
				z3 = -h_capa/2  - 3*(h_capa - h_ol) + h_ol
				# punto4
				x4 = -L_pro
				y4 = 0
				z4 = -h_capa/2  - 3*(h_capa - h_ol) + h_ol
				# punto5
				x5 = -L_pro + ol_drch
				y5 = 0
				z5 = -h_capa/2
				# punto6
				x6 = anchura/2
				y6 = 0
				z6 = -h_capa/2
				# punto7
				x7 = anchura/2 
				y7 = 0
				z7 = h_capa/2
				# punto8
				x8 = -L_pro + ol_drch
				y8 = 0
				z8 = h_capa/2
				# punto9
				x9 = -L_pro
				y9 = 0
				z9 = -h_capa/2  - 3*(h_capa - h_ol) + 2*h_ol
				# punto10
				x10 = -ol
				y10 = 0
				z10 = -h_capa/2  - 3*(h_capa - h_ol) + 2*h_ol
				# punto11
				x11 = -ol - ol_izd
				y11 = 0
				z11 = h_capa/2
				# punto12
				x12 = -anchura/2
				y12 = 0
				z12 = h_capa/2
				datos_ini_drch = np.array([-anchura - desf + mover_geometria - desf + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, x5, y5, z5, x6, y6, z6, x7, y7, z7, x8, y8, z8, x9, y9, z9, x10, y10, z10, x11, y11, z11, x12, y12, z12])
				datos_fin_drch = np.array([-anchura - desf + mover_geometria - desf + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, x5, y5, z5, x6, y6, z6, x7, y7, z7, x8, y8, z8, x9, y9, z9, x10, y10, z10, x11, y11, z11, x12, y12, z12])
				datos_input_tow = np.vstack((datos_ini_drch, datos_fin_drch))
				datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow== 0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - desf - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - desf - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria - desf + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - desf + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
					datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_1 = np.array([-ol_izd - ol + L_pro + mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_2 = np.array([-ol + L_pro+ mover_geometria,  -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_3 = np.array([mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_4 = np.array([mover_geometria + ol_drch, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_1, datos_2, datos_3, datos_4, datos_fin))
					datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow==0 or tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria+ abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 3.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		contador_par = 0
		contador_impar = 1
		if capa==5:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			tan_alph = math.tan(math.radians(angulos_tows[capa]))
			tan_beta = math.tan(math.radians(90 - angulos_tows[capa]))
			desf = -(anchura + L_pro)/2 + L_pro/2
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				# punto1_izd
				x1_izd = -anchura/2
				y1_izd = 0
				z1_izd = -h_capa/2
				# punto2_izd
				x2_izd = anchura/2 - ol - ol_izd + L_pro
				y2_izd = 0
				z2_izd = -h_capa/2
				# punto3_izd
				x3_izd = anchura/2 - ol + L_pro
				y3_izd = 0
				z3_izd = -h_capa/2  - 4*(h_capa - h_ol) + h_ol
				# punto4_izd
				x4_izd = anchura/2
				y4_izd = 0
				z4_izd = -h_capa/2  - 4*(h_capa - h_ol) + h_ol
				# punto5_izd
				x5_izd = anchura/2
				y5_izd = 0
				z5_izd = -h_capa/2  - 4*(h_capa - h_ol) + 2*h_ol
				# punto6_izd
				x6_izd = anchura/2 - ol + L_pro
				y6_izd = 0
				z6_izd = -h_capa/2  - 4*(h_capa - h_ol) + 2*h_ol
				# punto7_izd
				x7_izd = anchura/2 - ol - ol_izd + L_pro
				y7_izd = 0
				z7_izd = h_capa/2
				# punto8_izd
				x8_izd = -anchura/2
				y8_izd = 0
				z8_izd = h_capa/2
				datos_ini = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
				datos_fin = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_izd, y1_izd, z1_izd, x2_izd, y2_izd, z2_izd, x3_izd, y3_izd, z3_izd, x4_izd, y4_izd, z4_izd, x5_izd, y5_izd, z5_izd, x6_izd, y6_izd, z6_izd, x7_izd, y7_izd, z7_izd, x8_izd, y8_izd, z8_izd])
				datos_input_tow = np.vstack((datos_ini, datos_fin))
				datos_input.append(datos_input_tow)

				if L_pro<=ol_drch:
					beta = math.atan((5*h_ol - 4*h_capa)/ol_drch)
					# punto1_drch
					x1_drch = -anchura/2
					y1_drch = 0
					z1_drch = -h_capa/2 + (ol_drch - L_pro)*math.tan(beta)
					# punto2_drch
					x2_drch = -anchura/2 + ol_drch - L_pro
					y2_drch = 0
					z2_drch = -h_capa/2
					# punto3_drch
					x3_drch = anchura/2
					y3_drch = 0
					z3_drch = -h_capa/2
					# punto4_drch
					x4_drch = anchura/2
					y4_drch = 0
					z4_drch = h_capa/2
					# punto5_drch
					x5_drch = -anchura/2 + ol_drch - L_pro
					y5_drch = 0
					z5_drch = h_capa/2
					# punto6_drch
					x6_drch = -anchura/2
					y6_drch = 0
					z6_drch = -h_capa/2 + (ol_drch - L_pro)*math.tan(beta) + h_ol + ((L_pro)/ol_drch)*(h_capa - h_ol)
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, x1_drch, y1_drch, z1_drch, x2_drch, y2_drch, z2_drch, x3_drch, y3_drch, z3_drch, x4_drch, y4_drch, z4_drch, x5_drch, y5_drch, z5_drch, x6_drch, y6_drch, z6_drch])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)

				else:
					datos_ini = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom +seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_fin))
					datos_input.append(datos_input_tow)
				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow==0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
					datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_1 = np.array([-ol_izd - ol + L_pro + mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_2 = np.array([-ol + L_pro+ mover_geometria, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_3 = np.array([mover_geometria,  -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_seccion[capa]])
					datos_4 = np.array([mover_geometria + ol_drch, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
					datos_input_tow = np.vstack((datos_ini, datos_1, datos_2, datos_3, datos_4, datos_fin))
					datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow==0 or tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_ol_1 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol - ol_izd + L_pro)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_ol_2 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) - ol + L_pro), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) - ol + L_pro)*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_3 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1)), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1))*tan_alph, z/2.0 + z*capa - 4.5*(h_capa - h_ol) + h_ol, anchura, h_ol, angulos_tows[capa]])
						datos_ol_4 = np.array([x_ini_ang + mover_geometria + abs(x_ini_ang*(-1) + ol_drch), y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar + abs(x_ini_ang*(-1) + ol_drch)*tan_alph, z/2.0 + z*capa, anchura, h_capa, angulos_tows[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + desf/cos_alph - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_ol_1, datos_ol_2, datos_ol_3, datos_ol_4, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
		contador_par = 0 
		contador_impar = 0
		if capa==6:
			sin_alph = math.sin(math.radians(angulos_tows[capa]))
			cos_alph = math.cos(math.radians(angulos_tows[capa]))
			desf = 0
			desfase_array[capa] = desf
			if angulos_tows[capa]==0:
				mov_geometria_array[capa] = mover_geometria
				datos_ini_izd = np.array([-anchura - desf + mover_geometria, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_izd = np.array([-anchura - desf + mover_geometria, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_izd, datos_fin_izd))
				datos_input.append(datos_input_tow)

				datos_ini_drch = np.array([-anchura - desf + mover_geometria + repeticion, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_fin_drch = np.array([-anchura - desf + mover_geometria + repeticion, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
				datos_input_tow = np.vstack((datos_ini_drch, datos_fin_drch))
				datos_input.append(datos_input_tow)

				contador_izd = 1
				contador_drch = 1
				for tow in range(N_tows):
					if tow== 0 or tow%2==0:
						datos_ini = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria - repeticion*contador_izd, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_izd = contador_izd + 1
					else:
						datos_ini = np.array([-anchura - desf + mover_geometria + repeticion +  repeticion*contador_drch, -seed_XY + y_ini, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([-anchura - desf + mover_geometria + repeticion + repeticion*contador_drch, y_ini + Ldom + seed_XY, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_drch = contador_drch + 1
			elif angulos_tows[capa]==90:
				mov_geometria_array[capa] = mover_geometria90
				for tow in range(N_tows + 1):
						datos_ini = np.array([-Ldom/2.0 - seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([Ldom/2.0 + seed_XY, -Ldom/2.0 - desf + repeticion*tow + mover_geometria90, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
			elif angulos_tows[capa]<90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria + (repeticion/cos_alph)*contador_par + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang + mover_geometria - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria + 2*L*cos_alph, y_ini_ang + mover_geometria - (repeticion/cos_alph)*contador_impar + 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
			elif angulos_tows[capa]>90:
				mov_geometria_array[capa] = mover_geometria
				for tow in range(N_tows + 4):
					if tow%2==0:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria + (repeticion/cos_alph)*contador_par, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria + (repeticion/cos_alph)*contador_par - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_par = contador_par + 1
					else:
						datos_ini = np.array([x_ini_ang + mover_geometria, y_ini_ang*(-1) - mover_geometria - (repeticion/cos_alph)*contador_impar, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_fin = np.array([x_ini_ang + mover_geometria - 2*L*cos_alph, y_ini_ang*(-1) - mover_geometria - (repeticion/cos_alph)*contador_impar - 2*L*sin_alph, z/2.0 + z*capa, anchura, h_capa, angulos_seccion[capa]])
						datos_input_tow = np.vstack((datos_ini, datos_fin))
						datos_input.append(datos_input_tow)
						contador_impar = contador_impar + 1
	return datos_input, n_nodos, n_espesor, Ldom, desfase_array, mov_geometria_array
