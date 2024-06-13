import numpy as np

def writeAlyaFie(path, fileName, visco, Elementsetmaterials, numerodeelementos, Porosityfield_dir1_array,
                 Porosityfield_dir2_array,Porosityfield_dir3_array):
   """ Alya caseName.fie.dat file """

   # Material properties
   packing = 'hexa'  # 'quad' or 'hexa' packing
   if packing == 'quad':
       c = 57.0
       C1 = 16.0 / (9.0 * np.pi * np.sqrt(2.0))
       vf_max = np.pi / 4.0
   elif packing == 'hexa':
       c = 53.0
       C1 = 16.0 / (9.0 * np.pi * np.sqrt(6.0))
       vf_max = np.pi / (2.0 * np.sqrt(3.0))
   else:
       raise ValueError("NO SE HA SELECCIONADO PACKING")
    
   R_fibra = 2.5e-6  # metros

   # Filtrar elementos con materialId == 2
   material_ids = Elementsetmaterials[:, 1].astype(int)
   vf = Elementsetmaterials[:, 2]
   del Elementsetmaterials
   mask = (material_ids == 2)
   
   # Calcular k_lon y k_per vectorizados
   k_lon = (8.0 * R_fibra ** 2.0 * (1.0 - vf[mask]) ** 3.0) / (c * vf[mask])
   k_per = C1 * R_fibra ** 2.0 * (np.sqrt(vf_max / vf[mask]) - 1.0) ** (5.0 / 2.0)
   
   # Crear Sloc inversos vectorizados
   Sloc = np.zeros((mask.sum(), 3, 3))
   Sloc[:, 0, 0] = k_lon
   Sloc[:, 1, 1] = k_per
   Sloc[:, 2, 2] = k_per
   Sloc_inv = np.linalg.inv(Sloc)
   del Sloc, k_lon, k_per
   # Transformación tensorial local a global
   # Creación de matriz de transformación Q
   Q = np.zeros((Porosityfield_dir1_array[mask].shape[0], 3, 3))
   Q[:, :, 0] = Porosityfield_dir1_array[mask]
   Q[:, :, 1] = Porosityfield_dir2_array[mask]
   Q[:, :, 2] = Porosityfield_dir3_array[mask]
   del Porosityfield_dir1_array, Porosityfield_dir2_array, Porosityfield_dir3_array
   
   # Calcular Sglob
   Sglob = np.einsum('...ij,...jk,...kl->...il', Q.transpose(0, 2, 1), Sloc_inv, Q) * visco
   del Sloc_inv, Q
    # Crear líneas del archivo
   lines = ["FIELD= 1\n"]
   
   
   # Inicializar un contador para los índices de elementos que cumplen la condición
   idx_mask = 0

   for i in range(numerodeelementos):
       if mask[i]:
           if idx_mask < len(Sglob):
               lines.append(f'{i + 1} {Sglob[idx_mask, 0, 0]:1.8e} {Sglob[idx_mask, 1, 0]:1.8e} {Sglob[idx_mask, 2, 0]:1.8e} {Sglob[idx_mask, 0, 1]:1.8e} {Sglob[idx_mask, 1, 1]:1.8e} {Sglob[idx_mask, 2, 1]:1.8e} {Sglob[idx_mask, 0, 2]:1.8e} {Sglob[idx_mask, 1, 2]:1.8e} {Sglob[idx_mask, 2, 2]:1.8e}\n')
               idx_mask += 1
           else:
               # Esto es una verificación adicional para asegurarse de que no excedemos los límites
               print(f"Warning: idx_mask ({idx_mask}) exceeds Sglob size ({len(Sglob)})")
       else:
           lines.append(f'{i + 1} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e} {0.0:1.8e}\n')

   lines.append("END_FIELD\n")
   
   
   
    # Escribir todas las líneas al archivo de una vez
   with open(path + fileName + '.fie.dat', "w", newline='\n') as f:
       f.writelines(lines)

   
   
   return

def rotate_tensor_local_to_global_with_theta(Sloc, theta):
    # Rotation matrix
    Q = np.array([[ np.cos(theta),  np.sin(theta), 0.0],
                  [-np.sin(theta),  np.cos(theta), 0.0],
                  [          0.0,             0.0, 1.0]])
    
    # Rotate the tensor components
    Sglob = np.dot(np.dot(Q.T, Sloc), Q)
    return Sglob
