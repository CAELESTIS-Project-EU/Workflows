import numpy as np

def writeAlyaFie(path, fileName, visco, K11, K22, Elementsetmaterials, numerodeelementos, Porosityfield_dir1_array,
                 Porosityfield_dir2_array,Porosityfield_dir3_array):
    """ Alya caseName.fie.dat file
    """
    
    stream = open(path + fileName + '.fie.dat',"w", newline='\n')
    
    stream.write("FIELD= 1\n")

    Sloc = np.array([[ K11,   0.0,  0.0],
                     [ 0.0,   K22,  0.0],
                     [ 0.0,   0.0,  K22]])
    Sloc = np.linalg.inv(Sloc)
    
    for i in range(numerodeelementos):
        materialId = int(Elementsetmaterials[i][1])
        if materialId == 2:
            # Bulk
            # Transformation matrix
            u1 = Porosityfield_dir1_array[i,:]
            u2 = Porosityfield_dir2_array[i,:]
            u3 = Porosityfield_dir3_array[i,:]
            Q = np.column_stack((u1, u2, u3))
            # Tensor transformation from local to global
            Sglob = np.dot(np.dot(Q.T, Sloc), Q)*visco
            #Sglob = np.matmul(np.matmul(np.transpose(Q),Sloc), Q)*visco

            stream.write(f'{i+1} {Sglob[0][0]:1.8e} {Sglob[1][0]:1.8e} {Sglob[2][0]:1.8e} {Sglob[0][1]:1.8e} {Sglob[1][1]:1.8e} {Sglob[2][1]:1.8e} {Sglob[0][2]:1.8e} {Sglob[1][2]:1.8e} {Sglob[2][2]:1.8e}\n')
        else:
            # Gap
            stream.write(f'{i+1} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e}\n')
        
    stream.write("END_FIELD\n")
    stream.close()
    
    return

def rotate_tensor_local_to_global_with_theta(S_local, theta):
    # Rotation matrix
    Q = np.array([[ np.cos(theta),  np.sin(theta), 0.0],
                  [-np.sin(theta),  np.cos(theta), 0.0],
                  [          0.0,             0.0, 1.0]])
    
    # Rotate the tensor components
    Sglob = np.dot(np.dot(Q.T, Sloc), Q)
    return Sglob
