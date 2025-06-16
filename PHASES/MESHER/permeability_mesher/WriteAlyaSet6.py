
import numpy as np
import math

def AdjSets(n,dim,orden):
    neighbours = n*np.ones((2*orden+1)**2)
    dx = np.tile(np.arange(-orden, orden+1), (2*orden+1))
    dy = np.repeat(np.arange(-orden, orden+1)*dim, (2*orden+1))
    neighbours = neighbours + dx + dy
    return neighbours

def distancia_punto_recta(PuntosTow, PuntoCentroSet):
    # Obtener X1, Y1, Z1 del primer array en la lista
    puntoInicio = PuntosTow[0][:3]
    puntoFinal = PuntosTow[-1][:3]

    # Vector dirección de la recta
    direccion = puntoFinal[:2] - puntoInicio[:2]

    # Vector entre punto3 y punto1
    vector_punto3_punto1 = PuntoCentroSet[:2] - puntoInicio[:2]

    # Proyección del vector_punto3_punto1 sobre la dirección de la recta
    proyeccion = np.dot(vector_punto3_punto1, direccion) / np.dot(direccion, direccion) * direccion

    # Punto en la recta con el que estamos midiendo la distancia
    punto_en_recta = puntoInicio[:2] + proyeccion

    # Vector perpendicular
    vector_perpendicular = vector_punto3_punto1 - proyeccion

    # Distancia
    distancia = np.linalg.norm(vector_perpendicular)

    # Delante o detrás de la recta
    Xnegpos = round(PuntoCentroSet[0]-punto_en_recta[0],4)
    Ynegpos = round(PuntoCentroSet[1]-punto_en_recta[1],4)
    if Xnegpos<0:
        distancia *= -1
    if Xnegpos==0 and Ynegpos<0:
        distancia *= -1

    return distancia

def writeAlyaSet6(outputMeshPath, caseName, Lset, n_capas, nodes, L_pro, Ldom, volume_fraction,
                  ol, ol_izd, ol_drch, angulos_tows, w_tow, tipo_fallo, matriz_3dc_FVF, datos_input, matriz_4dc):
    Leltoxy = (np.max(nodes[:,0]) - np.min(nodes[:,0]))/(len(np.unique(nodes[:,0]))-1)
    # Leltoy = (np.max(nodes[:,1]) - np.min(nodes[:,1]))/(len(np.unique(nodes[:,1]))-1)
    Leltoz = (np.max(nodes[:,2]) - np.min(nodes[:,2]))/(len(np.unique(nodes[:,2]))-1)
    EpS = int(np.ceil(Lset/Leltoxy))
    LsetReal = EpS*Leltoxy
    Dom_x = np.max(nodes[:,0]) - np.min(nodes[:,0]) + Leltoxy
    Dom_y = np.max(nodes[:,1]) - np.min(nodes[:,1]) + Leltoxy
    Dom_z = np.max(nodes[:,2]) - np.min(nodes[:,2]) + Leltoz
    caso = int(caseName.replace('Case_',''))
    paso_z = (Dom_z) / (n_capas)
    H_set = paso_z
    EpC = int(np.ceil(H_set/Leltoz))
    n_sets_x = math.floor(Dom_x/LsetReal)
    paso_x = LsetReal
    n_sets_y = math.floor(Dom_y/LsetReal)
    paso_y = LsetReal
    # fvf2d = matriz_3dc_FVF.reshape([np.size(matriz_3dc_FVF)])
    centroids = np.c_[np.arange(len(nodes))+1, nodes]
    new_shape = (np.shape(matriz_4dc)[0],np.shape(matriz_4dc)[1],np.shape(matriz_4dc)[2],np.shape(matriz_4dc)[3]+1)
    centroids3d = np.reshape(centroids,new_shape)

    centroids3dfvf = np.append(centroids3d, np.reshape(matriz_3dc_FVF, [np.shape(centroids3d)[0],np.shape(centroids3d)[1],np.shape(centroids3d)[2],1]),axis = -1)

    to_write = []
    tows_xyz = []
    new_layer = []
    layerz = datos_input[0][0][2]
    for tow in datos_input:
        if tow[0][2] == layerz:
            new_layer.append(np.c_[tow[0][:3],tow[1][:3]].T)
        else:
            tows_xyz.append(new_layer)
            new_layer = [np.c_[tow[0][:3],tow[1][:3]].T]
            layerz = tow[0][2]
    tows_xyz.append(new_layer)
    lineas_pro = []


    for i, layer in enumerate(tows_xyz):
        for j in range(len(layer)-1):
            if angulos_tows[i] == 90 or (angulos_tows[i] == 0 and tipo_fallo == 'N'):
                # for i in range(len(layer)-1):
                lineas_pro.append(np.c_[(layer[j] + layer[j+1])/2])
            elif tipo_fallo != 'N' and i == 1:
                if j == 0:
                    linea_ol = np.c_[(layer[j] + layer[j+1])/2]
                    lineas_pro.append(np.c_[(layer[j] + layer[j+2])/2])
                elif j == 1:
                    linea_gap = np.c_[(layer[j] + layer[j+2])/2]
                else:
                    try:
                        lineas_pro.append(np.c_[(layer[j] + layer[j+2])/2])
                    except:
                        continue
            else:
                if j == 0:
                    lineas_pro.append(np.c_[(layer[j] + layer[j+1])/2])
                try:
                    lineas_pro.append(np.c_[(layer[j] + layer[j+2])/2])
                except:
                    continue

    setlist = []
    fvftow = volume_fraction*(w_tow+L_pro)/w_tow
    eset = 0
    s_ol = ol + ol_izd + ol_drch - L_pro



    for z in range(n_capas):
        z0 = (np.min(nodes[:,2]) - Leltoz/2) + z*paso_z
        z1 = z0 + H_set
        for y in range(n_sets_y):
            y0 = (np.min(nodes[:,1]) - Leltoxy/2) + y*paso_y
            y1 = y0 + LsetReal
            for x in range(n_sets_x):

                # inicio = time.time()
                elset = centroids3dfvf[x*EpS:(x+1)*EpS,y*EpS:(y+1)*EpS,z*EpC:(z+1)*EpC,:]
                x0 = (np.min(nodes[:,0]) - Leltoxy/2) + x*paso_x
                x1 = x0 + LsetReal
                eset += 1
                setfvf = 0
                for elto in np.reshape(elset,(int(np.size(elset)/np.shape(elset)[-1]),np.shape(elset)[-1])):
                    setfvf += elto[4]/len(np.reshape(elset,(int(np.size(elset)/np.shape(elset)[-1]),np.shape(elset)[-1])))
                    to_write.append(f'{str(int(elto[0]))} {str(eset)}\n')
                yset = (y1 + y0)/2
                xset = (x1 + x0)/2
                zset = (z1 + z0)/2
                point = np.array([xset, yset, zset])


                d_gap = 999
                d_gap1 = 999
                flag_ol = -1 #iniciamos los valores al por defecto
                flag_gap = -1
                flag_gap1 = -1
                d_ol = 999
                d_gap2 = 999
                s_gap = L_pro
                s_gap1 = L_pro
                set_span = (LsetReal/2*((angulos_tows[z]==0)+(angulos_tows[z]==90)) +
                        (LsetReal*2**0.5)/2 * ((angulos_tows[z] !=0 )*(angulos_tows[z] !=90)))

                #loop all tows guardando menor distancia
                #distancia al tow mas cercano es la menor distancia que salga, comparar con dmin
                #si mayor que dmin es gap
                pros_distancias_point=[]
                pros1_distancias_point=[]
                #CAMBIAR DISTANCIAS TOWS POR DISTANCIAS GAPS (O FALLOS) , GUARDAR DISTANCIA MÁS CERCANA REGARDLESSSSS
                for npro, pro in enumerate(lineas_pro):    # Numeros de tow (ntow) empieza a contar desde 0
                    capa=round((pro[0][2]+H_set/2)/H_set)-1
                    if z == capa:
                        pro_distancia = np.array([npro, distancia_punto_recta(pro, point)])
                        pros_distancias_point.append(pro_distancia)
                    elif ((z-capa)%n_capas == 1) or ((z-capa)%n_capas == (n_capas-1)):
                        pro_distancia1 = np.array([npro, distancia_punto_recta(pro, point)])
                        pros1_distancias_point.append(pro_distancia1)
                # Ordenar la lista por distancia
                pros_distancias_point.sort(key=lambda x: abs(x[1]))
                pros1_distancias_point.sort(key=lambda x: abs(x[1]))


                # Distancia al centro del gap más cercano (forma 2)
                d_gap = pros_distancias_point[0][1]
                d_gap1 = pros1_distancias_point[0][1]

                max_dis_Lpro = set_span + L_pro/2

                if abs(d_gap) < max_dis_Lpro:
                    flag_gap = 0
                if  abs(d_gap1) < max_dis_Lpro:
                    flag_gap1 = 0


                if tipo_fallo != 'N':
                    d_ol = distancia_punto_recta(linea_ol, point) - 2*distancia_punto_recta(linea_ol, point)*(tipo_fallo == 'G')
                    d_gap2 = distancia_punto_recta(linea_gap, point)
                    if abs(d_ol) < (s_ol/2 + set_span):
                        flag_ol = z - 1
                    if abs(d_gap2) < ((ol + L_pro)/2 + set_span) and z==1:
                        flag_gap = 0
                        d_gap = d_gap2
                        s_gap = ol + L_pro
                    elif abs(d_gap2) < ((ol + L_pro)/2 + set_span) and (z == 0 or z == 2):
                        flag_gap1 = 0
                        d_gap1 = d_gap2
                        s_gap1 = ol + L_pro
                    if abs(d_gap2) < abs(d_gap) and z==1:
                        d_gap = d_gap2
                        s_gap = ol + L_pro
                    elif abs(d_gap2) < abs(d_gap1) and (z == 0 or z == 2):
                        d_gap1 = d_gap2
                        s_gap1 = ol + L_pro
                else:
                    d_ol = 999

                normal = [0,0,-1]
                layer0 = [1,0,0]
                setlist.append([caso, eset, LsetReal, xset, yset, zset, z, H_set, fvftow, setfvf,] +
                               angulos_tows + normal + layer0 +
                               [zset, flag_gap, d_gap, s_gap, flag_ol, d_ol, s_ol, flag_gap1, d_gap1, s_gap1])




    totalsets = np.asarray(setlist)
    merged_sets = []
    nsetscapa = n_sets_x*n_sets_y
    iset = 1
    #GUARDAR FLAG MINIMA Y DISTANCIA AL 5
    for order in range(5):
        for set1 in totalsets:
            if  (order <= ((set1[1]-1)%nsetscapa)%n_sets_x < (n_sets_x - order)) and (order <= int(((set1[1]-1)%nsetscapa)/n_sets_y) < (n_sets_x-order)):
                neighbours = AdjSets(set1[1]-1,n_sets_x,order)
                setstomerge = totalsets[neighbours.astype(int)]
                setstomerge[:,-9] = np.max(setstomerge[:,-9])
                setstomerge[:,-8] = setstomerge[int(len(setstomerge)/2),-8]
                setstomerge[:,-7] = np.max(setstomerge[:,-7])
                setstomerge[:,-6] = np.max(setstomerge[:,-6])
                setstomerge[:,-5] = setstomerge[int(len(setstomerge)/2),-5]
                setstomerge[:,-3] = np.max(setstomerge[:,-3])
                setstomerge[:,-2] = setstomerge[int(len(setstomerge)/2),-2]


                setstomerge[:,2] = LsetReal*((2*order)+1)
                setstomerge[:,1] = iset
                iset += 1
                merged_sets.append(np.mean(setstomerge,axis = 0))
    merged_sets = np.asarray(merged_sets)



    with open(outputMeshPath+caseName+'.set.dat', 'w') as f:
        f.write("ELEMENTS\n")
        f.writelines(to_write)
        f.write("END_ELEMENTS\n")
        f.write("BOUNDARIES\n")
        f.write("END_BOUNDARIES\n")

    fmt = ''.join(['%i %i %9.5f %9.5f %9.5f %9.5f %i %9.5f %9.5f %9.5f '] + ['%4.2f,']*(len(angulos_tows)-1))
    fmt2 = fmt + ' %4.2f %9.5f,%9.5f,%9.5f %9.5f,%9.5f,%9.5f %9.5f %i %9.5f %9.5f %i %9.5f %9.5f %i %9.5f %9.5f'

    np.savetxt(outputMeshPath+'allsets.txt', merged_sets, fmt = fmt2 )


    return
