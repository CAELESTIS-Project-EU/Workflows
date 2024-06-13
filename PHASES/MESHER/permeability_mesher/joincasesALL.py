import numpy as np
import os
# import pandas as pd

def JoinCasesALL(casos_path, outdir, erase_previous = True):
    name_files = ['toRomallsets.csv']
    debug_headers = 'case;set;Lset;x;y;z;layer;h_tow;FVF_tow;FVF_set;llori;ilori;ulori;'
    gap_headers = 'gap;dgap;sgap;'
    ol_headers1 = 'ol;'
    ol_headers2 = 'dol;sol;adjgap;dadjgap;sadjgap;'
    out_headers = 'k1;k2;k3;pv1x;pv1y;pv1z;pv2x;pv2y;pv2z;Perm_xx;Perm_xy;Perm_xz;Perm_yy;Perm_yz;Perm_zz'
    for geom in name_files:     
        content = []
        for caso in os.listdir(casos_path):
            if geom.replace('csv', 'txt') in os.listdir(os.path.join(casos_path, str(caso))):
                file = os.path.join(casos_path, str(caso), geom.replace('csv', 'txt'))
                with open(file, 'r') as f:
                    for line in f:
                        content.append(line.split(' '))
        all_cases = np.asarray(content,dtype = float)            
        n_capas = 6
        oris = np.zeros([len(all_cases),3])
        for i, sets in enumerate(all_cases):
            oris[i,1] = sets[10+int((sets[6])%n_capas)]
            oris[i,0] = sets[10+int((sets[6]-1)%n_capas)]
            oris[i,2] = sets[10+int((sets[6]+1)%n_capas)]

        todebug = np.c_[all_cases[:,:10],oris,all_cases[:,10+n_capas+7:]]
        file_out2 = geom.replace('toRom', 'RawResults')
        np.savetxt(os.path.join(outdir,file_out2),todebug, delimiter = ';', header=debug_headers+gap_headers+ol_headers1+ol_headers2+out_headers, comments='')

    
