# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 09:34:26 2018

read the H5 file of Sysweld. Help may be found at http://docs.h5py.org/en/latest/quick.html

@author: yleguennec
"""

import h5py as h5py
from os import chdir
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class results_process:
    
    def __init__(self):
        self.file = ""
        self.dir = ""
        self.nodes_id = np.ndarray(())
        self.nodes_coord = np.ndarray(())
        self.nbre_states = 0
        self.nb_part = np.ndarray(())
        self.disp = np.ndarray(())
        self.connectivities = np.ndarray(())
        self.macro_voids = np.ndarray(())

    def read_erf_file(self, f):
        #chdir(self.dir)
        f = h5py.File(f, 'r')
        return f

    def close_erf_file(self, f):
        f.close()
        return None
        
        
    def extract_level(self, f, ID_extract, keys_glob, display_list = 0):
        list_keys_0 = list(f.keys())
        if display_list:
            print(list_keys_0)
        c_00 = f[list_keys_0[ID_extract]]
        keys_glob.append(list_keys_0[ID_extract])
        
        return c_00
        
    def extract_time(self, f):
        
        self.extract_nbre_instants(f)
        name_state = list(f['post/singlestate/'])
        vec_temps = np.zeros(self.nbre_states)
        for ijk_instant in range(self.nbre_states):
            vec_temps[ijk_instant] = list(f['post/singlestate/'+name_state[ijk_instant]+'/entityresults/NODE/Translational_Displacement/ZONE1_set1/erfblock/indexval'])[0]
        self.time_vec = vec_temps
        return None
        
        
    def extract_disp_node(self, f, ID_state):
        keys_glob = []
        print(ID_state)
        c_00 = self.extract_level(f, 1, keys_glob,0)
        c_000 = self.extract_level(c_00, 3, keys_glob)
        c_0000 = self.extract_level(c_000, ID_state, keys_glob)
        c_00000 = self.extract_level(c_0000, 0, keys_glob)
        c_000000 = self.extract_level(c_00000, 0, keys_glob)
        c_0000000 = self.extract_level(c_000000, 4, keys_glob)
        c_00000000 = self.extract_level(c_0000000, 0, keys_glob)
        c_000000000 = self.extract_level(c_00000000, 0, keys_glob)
        c_0000000000 = self.extract_level(c_000000000, 4, keys_glob)        
        
        print(keys_glob)
        print(c_0000000000.shape)
        val_c_0000000000 = c_0000000000[:]
        
        self.disp = val_c_0000000000
        
        return None

    def extract_coord_node(self, f):
        keys_glob = []
        nodes_id=np.asarray(f[u'post/constant/entityresults/NODE/COORDINATE/ZONE1_set0/erfblock/entid'])
        self.nodes_id = nodes_id
        self.nbre_nodes = len(nodes_id)
        
        nodes_coord=np.asarray(f[u'post/constant/entityresults/NODE/COORDINATE/ZONE1_set0/erfblock/res'])
        self.nodes_coord = nodes_coord[:, [0,1,2]]
        return None
        
    def extract_nbre_instants(self, f):
        self.nbre_states = len(list(f['post']['singlestate']))
        print("nb state")
        print(self.nbre_states)
        return self.nbre_states
        
    def extract_nbre_part(self,f):
        self.nb_part = np.asarray(f[u'post/constant/parts/PART/erfblock/pid'])
        print("nb state")
        print(self.nb_part)
        return None

    def extract_macro_void_and_write(self, f, output):
        nbre_states = len(list(f['post']['singlestate']))
        print("nb state")
        print(nbre_states)
        name_state = list(f['post/singlestate/'])
        macro_voids = np.zeros((self.nbre_nodes, nbre_states))
        for ijk_instant in range(nbre_states):
            res_t = f['post/singlestate/'+name_state[ijk_instant]+'/entityresults/NODE/MACRO_VOIDS/ZONE1_set0/erfblock/res']
            macro_voids[:,ijk_instant] = np.array(res_t).squeeze(1)
        self.macro_voids = macro_voids
        incfile= open(output,"w")
        for i in range(self.nbre_nodes):
            incfile.write(str(macro_voids[i, -1]))
            incfile.write("\n")

        incfile.close()
        

        
    
    def extract_connectivities(self, f):
        self.connectivities = np.asarray(f[u'post/constant/connectivities/TETRA4/erfblock/ic'])
        self.elem_id = np.asarray(f[u'post/constant/connectivities/TETRA4/erfblock/idele'])
        self.nbelem = len(self.elem_id)
        
        
        return None

    def plot_3D_brut(self):
                
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        ax.scatter(self.nodes_coord[:,0], self.nodes_coord[:,1], self.nodes_coord[:,2]+self.disp[:,-1], s=10, c = np.linalg.norm(self.disp,axis = 1))
        
        ax.axis('equal')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        

        plt.show()
        
        return None

    def extract_filling_factor(self,fid_f):
        name_state = list(fid_f['post/singlestate/'])
        filling_factor = np.zeros((self.nbre_nodes, self.nbre_states))
        for ijk_instant in range(self.nbre_states):
            res_t = fid_f['post/singlestate/'+name_state[ijk_instant]+'/entityresults/NODE/FILLING_FACTOR/ZONE1_set0/erfblock/res']
            filling_factor[:,ijk_instant] = np.array(res_t).squeeze(1)
        self.filling_factor = filling_factor
        return None
    
    def extract_data(self, fid_f, data_type):
        name_state = list(fid_f['post/singlestate/'])
        data = np.zeros((self.nbre_nodes, len(name_state)))
        for ijk_instant in range(len(name_state)):
            res_t = fid_f['post/singlestate/'+name_state[ijk_instant]+'/entityresults/NODE/' + str(data_type) + '/ZONE1_set0/erfblock/res']
            data[:,ijk_instant] = np.array(res_t).squeeze(1)
        self.data = data
        return None




    def save_res(self):
        fid_recap = open(self.dir + '\\res_ZF_num.txt', 'w')
        res_vec = [self.larg_001, self.larg_05, self.larg_09, self.penetration, self.longueur, self.mid_longueur, self.Tmax_8_4, self.Tmax_2_4, self.Tmax_23, self.Tmax_24_7, self.cooling_time_8_4, self.cooling_time_2_4, self.cooling_time_23, self.cooling_time_24_7, self.T_max_0_5_4, self.T_max_4_2_0, self.T_max_m4_2_0]
        np.savetxt(fid_recap, res_vec)
        fid_recap.close()
        return None


    def init_vtk(self):
        self.hash_table = []
        for i in range(max(self.nodes_id[:])+1):
            data = []
            data.append(i)
            data.append(-1)
            self.hash_table.append(data)

        for i in range(len(self.nodes_id)):
            self.hash_table[self.nodes_id[i]][1] = i
        fid_f = self.read_erf_file(self.f_file)
        fid_c = self.read_erf_file(self.c_file)
        fid_d = self.read_erf_file(self.d_file)

        f_nb_step = self.extract_nbre_instants(fid_f)
        c_nb_step = self.extract_nbre_instants(fid_c)
        d_nb_step = self.extract_nbre_instants(fid_d)
        
        max_step = max(f_nb_step, c_nb_step, d_nb_step)
        for i in range(max_step):
            print(i)
            self.write_vtk(str(i)) 
        print("ok")

    def write_vtk(self, step):
        incfile= open(self.vtkfilename + "_" + str(step) + ".vtk","w")
        incfile.write("# vtk DataFile Version 2.0\n") 
        incfile.write("shell.vtk, Created by yds\n") 
        incfile.write("ASCII\n") 
        incfile.write("DATASET UNSTRUCTURED_GRID\n") 
        incfile.write("POINTS ") 
        incfile.write(str(self.nbre_nodes))
        incfile.write(" double\n") 
        for i in range(self.nbre_nodes):
            incfile.write(str(self.nodes_coord[i,0]))
            incfile.write(" ")
            incfile.write(str(self.nodes_coord[i,1]))
            incfile.write(" ")
            incfile.write(str(self.nodes_coord[i,2]))
            incfile.write("\n")
        incfile.write("\n")
        incfile.write("CELLS ")
        incfile.write(str(self.nbelem))
        incfile.write(" ")
        incfile.write(str(5*self.nbelem))
        incfile.write("\n")
        for i in range(self.nbelem):
            incfile.write("4 ")
            incfile.write(str(self.hash_table[self.connectivities[i, 0]][1]))
            incfile.write(" ")
            incfile.write(str(self.hash_table[self.connectivities[i, 1]][1]))
            incfile.write(" ")
            incfile.write(str(self.hash_table[self.connectivities[i, 2]][1]))
            incfile.write(" ")
            incfile.write(str(self.hash_table[self.connectivities[i, 3]][1]))
            incfile.write("\n")
        incfile.write("\n")
        incfile.write("CELL_TYPES ")
        incfile.write(str(self.nbelem))
        incfile.write("\n")
        for i in range(self.nbelem):
            incfile.write("10 ")
        incfile.write("\n")
        # incfile.write("\n")
        # incfile.write("POINT_DATA ")
        # incfile.write(str(self.nbre_nodes))
        # incfile.write("\n")
        # incfile.write("FIELD FieldData 1")
        # incfile.write("\n")
        # incfile.write("1_disp_x 1 ")
        # incfile.write(str(self.nbre_nodes))
        # incfile.write(" double")
        # incfile.write("\n")
        # for i in range(self.nbre_nodes):
        #     if physic == "temperature":
        #         incfile.write(str(self.temperature_curing[i,int(step)]))
        #         incfile.write("\n")
        # incfile.write("\n")
        incfile.close()


    def add_data_to_vtk(self, type):
        fid_f = self.read_erf_file(self.f_file)
        fid_c = self.read_erf_file(self.c_file)
        fid_d = self.read_erf_file(self.d_file)

        f_nb_step = self.extract_nbre_instants(fid_f)
        c_nb_step = self.extract_nbre_instants(fid_c)
        d_nb_step = self.extract_nbre_instants(fid_d)
        
        max_step = max(f_nb_step, c_nb_step, d_nb_step)

        for k in range(len(type)):

            if type[k] == "f_temperature":            
                self.extract_data(fid_f, 'TEMPERATURE')
            if type[k] == "f_porosities":            
                self.extract_data(fid_f, 'MACRO_VOIDS')
            elif type[k] == "c_temperature":
                self.extract_data(fid_c, 'TEMPERATURE')
            elif type[k] == "f_pressure" :
                self.extract_data(fid_f, 'PRESSURE')
            elif type[k] == "f_filling_time" :
                self.extract_data(fid_f, 'MATERIAL_AGE')
            elif type[k] == "f_filling_factor":
                self.extract_data(fid_f, 'FILLING_FACTOR')
            elif type[k] == "c_alpha" :
                self.extract_data(fid_c, 'CURE')    
                 
            for i in range(max_step):
                if type[k] != "d_disp":
                    if (k == 0):
                        incfile= open(self.vtkfilename + "_" + str(i) + ".vtk","a")
                        incfile.write("\n")
                        incfile.write("POINT_DATA ")
                        incfile.write(str(self.nbre_nodes))
                        incfile.write("\n")
                        incfile.write("FIELD FieldData " + str(len(type)))
                        incfile.write("\n")
                        incfile.write(str(type[k]) + " 1 ")
                        incfile.write(str(self.nbre_nodes))
                        incfile.write(" double")
                        incfile.write("\n")
                    else:
                        incfile= open(self.vtkfilename + "_" + str(i) + ".vtk","a")
                        incfile.write("\n")
                        incfile.write(str(type[k]) + " 1 ")
                        incfile.write(str(self.nbre_nodes))
                        incfile.write(" double")
                        incfile.write("\n")      
                    
                    for j in range(self.nbre_nodes):
                        if type[k] == "f_temperature" or type[k] == "c_temperature":    
                            if i < (self.data.shape[1]):
                                incfile.write(str(self.data[j,int(i)]-273.15))
                                incfile.write("\n")
                            else:
                                incfile.write(str(self.data[j,-1]-273.15))
                                incfile.write("\n")
                        else:
                            if i < (self.data.shape[1]):
                                incfile.write(str(self.data[j,int(i)]))
                                incfile.write("\n")
                            else:
                                incfile.write(str(self.data[j,-1]))
                                incfile.write("\n")                           


                else:
                    if i < (d_nb_step):
                        self.extract_disp_node(fid_d, i)  
                        incfile= open(self.vtkfilename + "_" + str(i) + ".vtk","a")
                        incfile.write("\n")
                        incfile.write(str(type[k]) + " 3 ")
                        incfile.write(str(self.nbre_nodes))
                        incfile.write(" double")
                        incfile.write("\n")  
                        for j in range(self.nbre_nodes):
                            incfile.write(str(self.disp[j][0]))
                            incfile.write(" ")
                            incfile.write(str(self.disp[j][1]))
                            incfile.write(" ")
                            incfile.write(str(self.disp[j][2]))
                            incfile.write("\n")
                    else:
                        self.extract_disp_node(fid_d, d_nb_step-1)  
                        incfile= open(self.vtkfilename + "_" + str(i) + ".vtk","a")
                        incfile.write("\n")
                        incfile.write(str(type[k]) + " 3 ")
                        incfile.write(str(self.nbre_nodes))
                        incfile.write(" double")
                        incfile.write("\n")  
                        for j in range(self.nbre_nodes):
                            incfile.write(str(self.disp[j][0]))
                            incfile.write(" ")
                            incfile.write(str(self.disp[j][1]))
                            incfile.write(" ")
                            incfile.write(str(self.disp[j][2]))
                            
                            incfile.write("\n")

                
                incfile.write("\n")
                incfile.close()



if (__name__ == "__main__"):
    def extract_coord(self, filename):

        self.dir = "."
        self.file = filename
        fid_Y = self.read_erf_file()
        self.extract_coord_node(fid_Y)
        self.extract_nbre_instants(fid_Y)
        self.close_erf_file(fid_Y)


    def extract_temperature(self, filename):
        self.dir = "."
        self.file = filename
        fid_Y = self.read_erf_file()
        self.extract_temperature(fid_Y)
        self.close_erf_file(fid_Y)

    def extract_disp(self, filename):
        self.dir = "."
        self.file = filename
        fid_Y = self.read_erf_file()
        self.extract_temperature(fid_Y)
        self.extract_disp_node(fid_Y,1)

       
    def write_vtk(self):
       
        #objet_Y.extract_disp_node(fid_Y,1)    
        #objet_Y.extract_time(fid_Y)   
        #objet_Y.extract_filling_factor(fid_Y) 
        #objet_Y.extract_temperature(fid_Y)
        #objet_Y.close_erf_file(fid_Y)
        #objet_Y.plot_3D_brut()

        for i in range(max(self.nodes_id[:])+1):
            data = []
            data.append(i)
            data.append(-1)
            self.hash_table.append(data)

        for i in range(len(self.nodes_id)):
            self.hash_table[self.nodes_id[i]][1] = i
        for i in range(self.nbre_states):
            print(i)
            self.write_vtk(str(i)) 
        print("ok")



def extract_data_process_filling(inputFilePath, inputFileName, nbStepDist):
    objet_Y = results_process()
    objet_Y.dir = inputFilePath
    objet_Y.file = inputFileName
    fid_Y = objet_Y.read_erf_file()
    objet_Y.extract_coord_node(fid_Y)
    objet_Y.extract_nbre_instants(fid_Y)
    objet_Y.extract_disp_node(fid_Y,nbStepDist)    
    objet_Y.extract_time(fid_Y)    
    objet_Y.close_erf_file(fid_Y)
    #objet_Y.plot_3D_brut()
    
    return objet_Y.disp

def extract_num_step_filling(inputFilePath):
    objet_Y = results_process()
    objet_Y.file = inputFilePath
    fid_Y = objet_Y.read_erf_file(objet_Y.file)
    objet_Y.extract_nbre_instants(fid_Y)

    return objet_Y.nbre_states

def extract_num_part(inputFilePath):
    objet_Y = results_process()
    objet_Y.dir = inputFilePath
    objet_Y.file = inputFileName
    fid_Y = objet_Y.read_erf_file()
    objet_Y.extract_nbre_part(fid_Y)

    return objet_Y.nb_part

