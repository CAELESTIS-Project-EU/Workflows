import numpy as np
def FVF_variation(matriz_3dc_inout, n_capas, matriz_3dc_FVF, ajus_ol):
    ###################
    # Esta función solo vale para el caso específico actual donde aju_ol solo puede valer 5/6, la capa 1 no tiene defecto y la 7 tampoco tiene defecto
    ###################
    matriz_3dc_FVF_mod = np.copy(matriz_3dc_FVF)
    h_capa = int(len(matriz_3dc_inout[0,0,:])/n_capas)      # numero de elementos por capa
    for x in range(len(matriz_3dc_inout[:,0,0])):
        for y in range(len(matriz_3dc_inout[0,:,0])):
            flag_overlap = 0
            for capa in range(1,n_capas):  # La primera capa no se mira porque no puede haber overlap ahí
                if len(np.unique(matriz_3dc_inout[x,y,capa*h_capa:(capa+1)*h_capa])) != 1:
                    flag_overlap = 1
            if flag_overlap == 1:
                if n_capas<=6:
                    matriz_3dc_FVF_mod[x,y,1*h_capa:]=matriz_3dc_FVF[x,y,1*h_capa:]/ajus_ol
                elif n_capas>6:
                    matriz_3dc_FVF_mod[x,y,1*h_capa:6*h_capa]=matriz_3dc_FVF[x,y,1*h_capa:6*h_capa]/ajus_ol
                flag_overlap = 0
    return matriz_3dc_FVF_mod
