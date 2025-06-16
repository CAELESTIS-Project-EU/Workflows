import numpy as np
import math
def writeAlyaSet2(path, fileName, L_set, n_capas, nodes):
    Leltox = (np.max(nodes[:,0]) - np.min(nodes[:,0]))/(len(np.unique(nodes[:,0]))-1)
    Leltoy = (np.max(nodes[:,1]) - np.min(nodes[:,1]))/(len(np.unique(nodes[:,1]))-1)
    Leltoz = (np.max(nodes[:,2]) - np.min(nodes[:,2]))/(len(np.unique(nodes[:,2]))-1)
    
    Dom_x = np.max(nodes[:,0]) - np.min(nodes[:,0]) + Leltox
    Dom_y = np.max(nodes[:,1]) - np.min(nodes[:,1]) + Leltoy
    Dom_z = np.max(nodes[:,2]) - np.min(nodes[:,2]) + Leltoz
    
    paso_z = (Dom_z) / (n_capas)
    H_set = paso_z
    n_sets_x = math.ceil(Dom_x/L_set)
    paso_x = (Dom_x - L_set) / (n_sets_x - 1)
    n_sets_y = math.ceil(Dom_y/L_set)
    paso_y = (Dom_y - L_set) / (n_sets_y - 1)
    
    
    
    #Calculo de la coordenada de los centroides de los elementos, cargar coordenadas de cada nodo en una nueva dimension
    #y colapsar segun la media de la nueva dimension, copiar numero de elto para que la media salga lo mismo
    #115 sec 8.326104 e6 eltos
    
    # elemxyz = np.zeros([len(elements),len(elements[0])-1,4])
    # for i, elem in enumerate(elements):
    #     elemxyz[i,:,0] = elem[0]
    #     for j, node in enumerate(elem[1:]):
    #         elemxyz[i,j,1:] = nodes[int(node-1),1:] 
    # centroids = np.mean(elemxyz,axis = 1)
    centroids = np.c_[np.arange(len(nodes))+1, nodes]
    
    #Escritura de los sets, para las coordenadas de cada set filtrar los elementos cuyo
    #centroide cae en el interior hacerlo en dos pasos porque la primera dimension descarta
    #muchos nodos ya de entrada. 85 sec 8.326104 e6 eltos 676 sets
    setscoord = []
    eset = 0
    stream = open(path+fileName+'.set.dat', 'w', newline='\n')

    stream.write("ELEMENTS\n")
#    for i in centroids:
#        stream.write(f'{str(int(i[0]))} {1}\n') 
    for z in range(n_capas):
        z0 = (np.min(nodes[:,2]) - Leltoz/2) + z*paso_z
        z1 = z0 + H_set
        for y in range(n_sets_y):
            y0 = (np.min(nodes[:,1]) - Leltoy/2) + y*paso_y
            y1 = y0 + L_set
            for x in range(n_sets_x):
                x0 = (np.min(nodes[:,0]) - Leltox/2) + x*paso_x
                x1 = x0 + L_set
                eset += 1
                elset = centroids[(centroids[:,1] > x0) * (centroids[:,1] < x1)]
                elset = elset[(elset[:,2] > y0) * (elset[:,2] < y1) * (elset[:,3] > z0) * (elset[:,3] < z1)]
                for elto in elset:
                    # f.write(str(int(elto[0])) + ' ' + str(eset) + '\n')
                    stream.write(f'{str(int(elto[0]))} {str(eset)}\n') 
                    setscoord.append([eset,x0,x1,y0,y1,z0,z1])

    
    setscoord = np.asarray(setscoord)
    fmt = ' '.join(['%i'] + ['%9.5f']*6)
    np.savetxt(path+'setscoord.txt', setscoord, fmt = fmt)

    # for i in range(0,nelem):
    #     stream.write(f'{i+1} {1}\n')   
    stream.write("END_ELEMENTS\n")
    
    stream.write("BOUNDARIES\n")
    stream.write("END_BOUNDARIES\n")

        
