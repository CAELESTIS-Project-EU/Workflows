import numpy as np
import math
def AdjSets(n,dim,orden):
    neighbours = n*np.ones((2*orden+1)**2)
    dx = np.tile(np.arange(-orden, orden+1), (2*orden+1))
    dy = np.repeat(np.arange(-orden, orden+1)*dim, (2*orden+1))
    neighbours = neighbours + dx + dy
    return neighbours
def writeAlyaSet4(outputMeshPath, caseName, Lset, n_capas, nodes, L_pro, Ldom, mov_geometria_array,
                  ol, ol_izd, ol_drch, desfase_array, angulos_tows, w_tow, tipo_fallo, matriz_3dc_FVF):
    Leltox = (np.max(nodes[:,0]) - np.min(nodes[:,0]))/(len(np.unique(nodes[:,0]))-1)
    Leltoy = (np.max(nodes[:,1]) - np.min(nodes[:,1]))/(len(np.unique(nodes[:,1]))-1)
    Leltoz = (np.max(nodes[:,2]) - np.min(nodes[:,2]))/(len(np.unique(nodes[:,2]))-1)

    Dom_x = np.max(nodes[:,0]) - np.min(nodes[:,0]) + Leltox
    Dom_y = np.max(nodes[:,1]) - np.min(nodes[:,1]) + Leltoy
    Dom_z = np.max(nodes[:,2]) - np.min(nodes[:,2]) + Leltoz
    caso = int(caseName.replace('case_',''))
    paso_z = (Dom_z) / (n_capas)
    H_set = paso_z
    n_sets_x = math.floor(Dom_x/Lset)
    paso_x = Lset
    n_sets_y = math.floor(Dom_y/Lset)
    paso_y = Lset
    fvf2d = matriz_3dc_FVF.reshape([np.size(matriz_3dc_FVF)])
    centroids = np.c_[np.arange(len(nodes))+1, nodes]

    #Escritura de los sets, para las coordenadas de cada set filtrar los elementos cuyo
    #centroide cae en el interior hacerlo en dos pasos porque la primera dimension descarta
    #muchos nodos ya de entrada. 85 sec 8.326104 e6 eltos 676 sets


    stream = open(outputMeshPath+caseName+'.set.dat', 'w', newline='\n')
    pi = math.pi
    stream.write("ELEMENTS\n")
#    for i in centroids:
#        stream.write(f'{str(int(i[0]))} {1}\n')
    setlist = []
    eset = 0
    for z in range(n_capas):
        z0 = (np.min(nodes[:,2]) - Leltoz/2) + z*paso_z
        z1 = z0 + H_set
        for y in range(n_sets_y):
            y0 = (np.min(nodes[:,1]) - Leltoy/2) + y*paso_y
            y1 = y0 + Lset
            for x in range(n_sets_x):
                x0 = (np.min(nodes[:,0]) - Leltox/2) + x*paso_x
                x1 = x0 + Lset
                eset += 1
                elset = centroids[(centroids[:,1] > x0) * (centroids[:,1] < x1)]
                elset = elset[(elset[:,2] > y0) * (elset[:,2] < y1) * (elset[:,3] > z0) * (elset[:,3] < z1)]
                setfvf = 0
                for elto in elset:
                    # f.write(str(int(elto[0])) + ' ' + str(eset) + '\n')
                    setfvf += fvf2d[int(elto[0])-1]/len(elset)
                    stream.write(f'{str(int(elto[0]))} {str(eset)}\n')
                rep = w_tow + L_pro
                desf = mov_geometria_array[z] - desfase_array[z]
                yset = (y1 + y0)/2
                xset = (x1 + x0)/2

                # d_ori = xset*(angulos_tows[z]==0) + yset*(angulos_tows[z]==90) + ((xset**2 + yset**2)**0.5 * ((angulos_tows[z] !=0 )* (angulos_tows[z] !=90)))
                d_ori = abs(xset*math.sin(pi*angulos_tows[z]/180) + yset*math.cos(pi*angulos_tows[z]/180)) #coordenada 1d del punto (distancia a linea central)
                s_ol = ol + ol_izd + ol_drch - L_pro
                d_gap = Ldom
                d_pro = Ldom
                loc_pro = 0
                flag_ol = -1 #iniciamos los valores al por defecto
                flag_gap = -1
                s_gap = L_pro
                d_ol = xset - ((L_pro + ol_drch - ol_izd - ol) + (ol_drch - mov_geometria_array[z]))/2

                dmin = ((L_pro + Lset)/2*((angulos_tows[z]==0) + (angulos_tows[z]==90)) +
                        (L_pro + Lset*2**0.5)/2 * ((angulos_tows[z] !=0 )* (angulos_tows[z] !=90)))
                if tipo_fallo == 'N':
                    if angulos_tows[z] == 0 or angulos_tows[z] == 90:
                        loc_pro = -Ldom/2 + desf - rep/2
                    else:
                        loc_pro = rep/2*(z%2)
                    d_pro = rep/2 - abs((d_ori-loc_pro)%rep - rep/2)
                    if abs(d_pro) < dmin:
                        flag_gap = 0
                    d_gap = d_pro
                elif tipo_fallo == 'O':
                    d_ol = xset - ((L_pro + ol_drch - ol_izd - ol) + (ol_drch - mov_geometria_array[z]))/2
                    s_ol = ol + ol_izd + ol_drch - L_pro
                    if z == 1:
                        loc_pro = w_tow/2 + desf
                    elif angulos_tows[z] == 90:
                        loc_pro = - Ldom/2 + desf
                    elif angulos_tows[z] == 0:
                        loc_pro = 0
                    else:
                        loc_pro = rep/2*(z%2)
                    d_pro = rep/2 - abs((d_ori-loc_pro)%rep - rep/2)
                    if abs(d_pro) < dmin:
                        flag_gap = 0
                        d_gap = d_pro
                    if (ol_drch - mov_geometria_array[z]) > xset > (L_pro + ol_drch - ol_izd - ol):
                        flag_ol = z - 1
                    elif z == 1 and ((w_tow + L_pro - ol) < xset < (w_tow + 2*L_pro)):
                        flag_gap = 0
                        d_gap = xset - ((w_tow + L_pro - ol) + (w_tow + 2*L_pro))/2
                        s_gap = ol + L_pro
                    if abs(xset - ((w_tow + L_pro - ol) + (w_tow + 2*L_pro))/2) < d_pro:
                        d_gap = xset - ((w_tow + L_pro - ol) + (w_tow + 2*L_pro))/2
                elif tipo_fallo == 'G':
                    if z == 1:
                        loc_pro = w_tow/2 + desf
                    elif angulos_tows[z] == 90:
                        loc_pro = - Ldom/2 + desf
                    elif angulos_tows[z] == 0:
                        loc_pro = 0
                    else:
                        loc_pro = rep/2*(z%2)
                    d_pro = rep/2 - abs((d_ori-loc_pro)%rep - rep/2)
                    if abs(d_pro) < dmin:
                        flag_gap = 0
                        d_gap = d_pro
                    if (ol_drch - mov_geometria_array[z]) > xset > (L_pro + ol_drch - ol_izd - ol):
                        flag_ol = z - 1
                    elif z == 1 and ((w_tow + L_pro - ol) < xset < (w_tow + 2*L_pro)):
                        flag_gap = 0
                        d_gap = xset - ((w_tow + L_pro - ol) + (w_tow + 2*L_pro))/2
                        s_gap = ol + L_pro
                    if abs(xset - ((w_tow + L_pro - ol) + (w_tow + 2*L_pro))/2) < d_pro:
                        d_gap = xset - ((w_tow + L_pro - ol) + (w_tow + 2*L_pro))/2
                normal = [0,0,-1]
                layer0 = [1,0,0]
                setlist.append([caso, eset, Lset, (x0+x1)/2,(y0+y1)/2,(z0+z1)/2,z, setfvf] + angulos_tows + normal +
                                layer0 + [(z0+z1)/2, flag_gap,d_gap,s_gap,flag_ol,d_ol,s_ol])
    # for i in range(0,nelem):
    #     stream.write(f'{i+1} {1}\n')
    stream.write("END_ELEMENTS\n")

    stream.write("BOUNDARIES\n")
    stream.write("END_BOUNDARIES\n")

    totalsets = np.asarray(setlist)
    merged_sets = []
    nsetscapa = n_sets_x*n_sets_y
    iset = 1
    for order in range(3):
        for set1 in totalsets:
            if  (order <= (set1[1]%nsetscapa)%n_sets_x < (n_sets_x - order)) and (order <= int((set1[1]%nsetscapa)/n_sets_y) < (n_sets_x-order)):
                neighbours = AdjSets(set1[1]-1,n_sets_x,order)
                setstomerge = totalsets[neighbours.astype(int)]
                setstomerge[:,-6] = np.max(setstomerge[:,-6])
                setstomerge[:,-3] = np.max(setstomerge[:,-3])
                setstomerge[:,-4] = np.max(setstomerge[:,-4])
                setstomerge[:,2] = Lset*((2*order)+1)
                setstomerge[:,1] = iset
                iset += 1
                merged_sets.append(np.mean(setstomerge,axis = 0))
    merged_sets = np.asarray(merged_sets)


    # if len(oli0) + len(ol1) + len(olMgap) + len(olM) + len(olgap) + len(alltow) != len(totalsets):
    #     print('faltan o sobran sets')
    # else:
    #     print('pinta bien')

    # fmt = ' '.join(['%i'] + ['%9.5f']*6)
    fmt = ''.join(['%i %i %9.5f %9.5f %9.5f %9.5f %i %9.5f '] + ['%4.2f,']*(len(angulos_tows)-1))
    fmt2 = fmt + ' %4.2f %9.5f,%9.5f,%9.5f %9.5f,%9.5f,%9.5f %9.5f %i %9.5f %9.5f %i %9.5f %9.5f'
    fmt1 = fmt + ' %4.2f %9.5f,%9.5f,%9.5f %9.5f,%9.5f,%9.5f %9.5f %i %9.5f %9.5f'
    fmt0 = fmt + ' %4.2f %9.5f,%9.5f,%9.5f %9.5f,%9.5f,%9.5f %9.5f'

    alltow = merged_sets[np.all(np.c_[merged_sets[:,-6] == -1 , merged_sets[:,-3] == -1], axis = 1), :-6]
    np.savetxt(outputMeshPath+'alltow.txt', alltow, fmt = fmt0 )

    gap0 = merged_sets[np.all(np.c_[merged_sets[:,-6] == 0, merged_sets[:,-3] == -1], axis = 1) , :-3]
    np.savetxt(outputMeshPath+'gap0.txt', gap0, fmt = fmt1 )

    ol0 = merged_sets[merged_sets[:,-3] == 0]
    if len(ol0) > 0:
        ol0 = np.delete(ol0, [-6, -5, -4], 1)
        np.savetxt(outputMeshPath+'ol0.txt', ol0, fmt = fmt1 )
    else:
        np.savetxt(outputMeshPath+'ol0.txt', ol0, fmt = fmt2 )

    ol1 = merged_sets[merged_sets[:,-3] == 1]
    if len(ol1) > 0:
        ol1 = np.delete(ol1, [-6, -5, -4], 1)
        np.savetxt(outputMeshPath+'ol1.txt', ol1, fmt = fmt1 )
    else:
        np.savetxt(outputMeshPath+'ol1.txt', ol1, fmt = fmt2 )

    olM = merged_sets[np.all(np.c_[merged_sets[:,-6] == -1 , merged_sets[:,-3] > 1], axis = 1)]
    if len(olM) > 0:
        olM = np.delete(olM, [-6, -5, -4], 1)
        np.savetxt(outputMeshPath+'olM.txt', olM, fmt = fmt1 )
    else:
        np.savetxt(outputMeshPath+'olM.txt', olM, fmt = fmt2 )

    olMgap = merged_sets[np.all(np.c_[merged_sets[:,-6] == 0 , merged_sets[:,-3] > 1], axis = 1)]
    np.savetxt(outputMeshPath+'olMgap.txt', olMgap, fmt = fmt2 )
