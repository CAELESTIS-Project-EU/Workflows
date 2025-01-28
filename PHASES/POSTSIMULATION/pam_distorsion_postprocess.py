import h5py
import shutil
import numpy as np
import os
from pycompss.api.task import task
from pycompss.api.parameter import DIRECTORY_IN
from pycompss.api.api import compss_delete_file

def run(line, step, rtm_folder, curing_folder, distorsion_folder, in_file_rtm, in_file_dis,path_out, 
                 file_IN1, file_IN2, prefix, file_OUT1, file_OUT2, clean):
    reduce_erfh5(line,step,rtm_folder,in_file_rtm,distorsion_folder,in_file_dis,path_out)
    save_RTM_res(line,distorsion_folder,file_IN1,file_IN2,path_out,prefix,file_OUT1,file_OUT2)
    if bool(clean):
        compss_delete_file(rtm_folder)
        compss_delete_file(curing_folder)
        compss_delete_file(distorsion_folder)
    
    

@task(distorsion_folder = DIRECTORY_IN)
def save_RTM_res(line,distorsion_folder,file_IN1,file_IN2,path_out,prefix,file_OUT1,file_OUT2): #(shutil, os)
    if not os.path.exists(path_out): 
        os.makedirs(path_out)
    #COPY 1
    src_file = os.path.join(distorsion_folder,file_IN1)
    dest_file = os.path.join(path_out,prefix +str(line)+file_OUT1)
    shutil.copy(src_file, dest_file)
    #COPY 2
    src_file = os.path.join(distorsion_folder,file_IN2)
    dest_file = os.path.join(path_out,prefix +str(line)+file_OUT2)
    shutil.copy(src_file, dest_file)


@task(rtm_folder = DIRECTORY_IN, distorsion_folder = DIRECTORY_IN)
def reduce_erfh5(line,step,rtm_folder,in_file_rtm,distorsion_folder,in_file_dis, path_out):
    step = int(step)
    if not os.path.exists(path_out): 
        os.makedirs(path_out)
    #VOID
    f = h5py.File(os.path.join(rtm_folder,in_file_rtm), 'r')
    name_state = list(f['post/singlestate/'])
    void = np.array(f["post/singlestate/"+name_state[step]+"/entityresults/NODE/MACRO_VOIDS/ZONE1_set0/erfblock/res"])
    np.savetxt(path_out+"void"+str(line)+".txt",void)
    #DISP
    f = h5py.File(os.path.join(distorsion_folder,in_file_dis), 'r')
    name_state = list(f['post/singlestate/'])
    disp = np.array(f["post/singlestate/"+name_state[step]+"/entityresults/NODE/Translational_Displacement/ZONE1_set1/erfblock/res"])
    np.savetxt(path_out+"disp"+str(line)+".csv",disp)
