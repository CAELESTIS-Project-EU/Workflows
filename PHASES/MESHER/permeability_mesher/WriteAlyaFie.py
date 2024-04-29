import numpy as np

def writeAlyaFie(path, fileName, visco, volume_fraction, Elementsetmaterials, numerodeelementos, Porosityfield_dir1_array,
                 Porosityfield_dir2_array,Porosityfield_dir3_array):
    """ Alya caseName.fie.dat file
    """
    
	# Material properties
    packing = 'hexa' # 'quad' or 'hexa' packing
    if packing == 'quad':
        c = 57.0
        C1 = 16.0/(9.0*np.pi*np.sqrt(2.0))
        vf_max = np.pi/4.0
    elif packing == 'hexa':
        c = 53.0
        C1 = 16.0/(9.0*np.pi*np.sqrt(6.0))
        vf_max = np.pi/(2.0*np.sqrt(3.0))
    else:
        print("NO SE HA SELECCIONADO PACKING")
    R_fibra = 2.5e-6 # metros
    
    
    stream = open(path + fileName + '.fie.dat',"w", newline='\n')
    
    stream.write("FIELD= 1\n")

    
    for i in range(numerodeelementos):
        materialId = int(Elementsetmaterials[i][1])
        if materialId == 2:
            k_lon     = (8.0*R_fibra**2.0*(1.0-volume_fraction)**3.0)/(c*volume_fraction)
            k_per     = C1*R_fibra**2.0*(np.sqrt(vf_max/volume_fraction)-1.0)**(5.0/2.0)
            
            Sloc = np.array([[ k_lon,   0.0,  0.0],
                             [ 0.0,   k_per,  0.0],
                             [ 0.0,   0.0,  k_per]])
            Sloc = np.linalg.inv(Sloc)
            
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

def rotate_tensor_local_to_global_with_theta(Sloc, theta):
    # Rotation matrix
    Q = np.array([[ np.cos(theta),  np.sin(theta), 0.0],
                  [-np.sin(theta),  np.cos(theta), 0.0],
                  [          0.0,             0.0, 1.0]])
    
    # Rotate the tensor components
    Sglob = np.dot(np.dot(Q.T, Sloc), Q)
    return Sglob
