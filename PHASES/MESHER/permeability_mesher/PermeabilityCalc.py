import numpy as np

def Permeability_Calculation(gravity, density, viscosity, resultados):
    # Definir las medias de velocidad y presión para cada dirección de flujo
    Vx_mean = np.zeros(3)
    Vy_mean = np.zeros(3)
    Vz_mean = np.zeros(3)
    
    Px_mean = np.zeros(3)
    Py_mean = np.zeros(3)
    Pz_mean = np.zeros(3)
    # X-flow
    Vx_mean[0] = resultados[0]
    Vy_mean[0] = resultados[1]
    Vz_mean[0] = resultados[2]
    # Y-flow
    Vx_mean[1] = resultados[6]
    Vy_mean[1] = resultados[7]
    Vz_mean[1] = resultados[8]
    # Z-flow
    Vx_mean[2] = resultados[12]
    Vy_mean[2] = resultados[13]
    Vz_mean[2] = resultados[14]

    # X-flow
    Px_mean[0] = resultados[3]
    Py_mean[0] = resultados[4]
    Pz_mean[0] = resultados[5]
    # Y-flow
    Px_mean[1] = resultados[9]
    Py_mean[1] = resultados[10]
    Pz_mean[1] = resultados[11]
    # Z-flow
    Px_mean[2] = resultados[15]
    Py_mean[2] = resultados[16]
    Pz_mean[2] = resultados[17]
    
    dPressure = np.array([[Px_mean[0]+gravity*density,Py_mean[0],Pz_mean[0],0,0,0,0,0,0],
                         [0,0,0,Px_mean[0]+gravity*density,Py_mean[0],Pz_mean[0],0,0,0],
                         [0,0,0,0,0,0,Px_mean[0]+gravity*density,Py_mean[0],Pz_mean[0]],
                         [Px_mean[1],Py_mean[1]+gravity*density,Pz_mean[1],0,0,0,0,0,0],
                         [0,0,0,Px_mean[1],Py_mean[1]+gravity*density,Pz_mean[1],0,0,0],
                         [0,0,0,0,0,0,Px_mean[1],Py_mean[1]+gravity*density,Pz_mean[1]],
                         [Px_mean[2],Py_mean[2],Pz_mean[2]+gravity*density,0,0,0,0,0,0],
                         [0,0,0,Px_mean[2],Py_mean[2],Pz_mean[2]+gravity*density,0,0,0],
                         [0,0,0,0,0,0,Px_mean[2],Py_mean[2],Pz_mean[2]+gravity*density]])
    Velocity = np.array([Vx_mean[0],
                         Vy_mean[0],
                         Vz_mean[0],
                         Vx_mean[1],
                         Vy_mean[1],
                         Vz_mean[1],
                         Vx_mean[2],
                         Vy_mean[2],
                         Vz_mean[2]])    

    Permeability_tensor = np.linalg.solve(dPressure, Velocity)
    Permeability_tensor = Permeability_tensor*viscosity
    Permeability_tensor = Permeability_tensor.reshape((3, 3))
    Permeability_tensor_symmetric = (Permeability_tensor + Permeability_tensor.T) / 2.0
    # Calcula los valores propios y los vectores propios
    eigenvalues, eigenvectors = np.linalg.eig(Permeability_tensor_symmetric)
    # Ordena los valores propios de mayor a menor
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]
        
    # Redondear los vectores
    # eigenvectors = np.round(eigenvectors, decimals=3)
    
    return eigenvalues, eigenvectors[:,0], eigenvectors[:,1]

def Permeability_Calculation_sim(gravity, density, viscosity, resultados):
    # Definir las medias de velocidad y presión para cada dirección de flujo
    Vx_mean = np.zeros(3)
    Vy_mean = np.zeros(3)
    Vz_mean = np.zeros(3)
    
    Px_mean = np.zeros(3)
    Py_mean = np.zeros(3)
    Pz_mean = np.zeros(3)
    
    # Asignar los valores medios de velocidad y presión de las simulaciones CFD
    Vx_mean[0] = resultados[0]
    Vy_mean[0] = resultados[1]
    Vz_mean[0] = resultados[2]
    
    Vx_mean[1] = resultados[6]
    Vy_mean[1] = resultados[7]
    Vz_mean[1] = resultados[8]
    
    Vx_mean[2] = resultados[12]
    Vy_mean[2] = resultados[13]
    Vz_mean[2] = resultados[14]

    Px_mean[0] = resultados[3]
    Py_mean[0] = resultados[4]
    Pz_mean[0] = resultados[5]
    
    Px_mean[1] = resultados[9]
    Py_mean[1] = resultados[10]
    Pz_mean[1] = resultados[11]
    
    Px_mean[2] = resultados[15]
    Py_mean[2] = resultados[16]
    Pz_mean[2] = resultados[17]
    
    # Construir la matriz de diferencia de presión (9x6)
    dPressure = np.array([[Px_mean[0]+gravity*density,Py_mean[0],Pz_mean[0],0,0,0],
                         [0,Px_mean[0]+gravity*density,0,Py_mean[0],Pz_mean[0],0],
                         [0,0,Px_mean[0]+gravity*density,0,Py_mean[0],Pz_mean[0]],
                         [Px_mean[1],Py_mean[1]+gravity*density,Pz_mean[1],0,0,0],
                         [0,Px_mean[1],0,Py_mean[1]+gravity*density,Pz_mean[1],0],
                         [0,0,Px_mean[1],0,Py_mean[1]+gravity*density,Pz_mean[1]],
                         [Px_mean[2],Py_mean[2],Pz_mean[2]+gravity*density,0,0,0],
                         [0,Px_mean[2], 0,Py_mean[2],Pz_mean[2]+gravity*density,0],
                         [0,0,Px_mean[2], 0,Py_mean[2],Pz_mean[2]+gravity*density]])

    
    # Construir el vector de velocidad (9x1)
    Velocity = np.array([
        Vx_mean[0], Vy_mean[0], Vz_mean[0],
        Vx_mean[1], Vy_mean[1], Vz_mean[1],
        Vx_mean[2], Vy_mean[2], Vz_mean[2]
    ])
    
    # Resolver el sistema sobredeterminado mediante mínimos cuadrados
    scale = 1e9
    Velocity *= scale
    dPressure *= scale
    Permeability_tensor, _, _, _ = np.linalg.lstsq(dPressure, Velocity, rcond=None)
    Permeability_tensor = Permeability_tensor*viscosity
    Permeability_tensor_3x3 = np.array([[Permeability_tensor[0], Permeability_tensor[1], Permeability_tensor[2]],
                                    [Permeability_tensor[1], Permeability_tensor[3], Permeability_tensor[4]],
                                    [Permeability_tensor[2], Permeability_tensor[4], Permeability_tensor[5]]])
    Permeability_tensor_3x3 *= scale
    
    # Calcula los valores propios y los vectores propios
    eigenvalues, eigenvectors = np.linalg.eig(Permeability_tensor_3x3)
    # Ordena los valores propios de mayor a menor
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvalues /= scale
    eigenvectors = eigenvectors[:, sorted_indices]
    eigenvectors /= scale
        
    
    return eigenvalues, eigenvectors[:,0], eigenvectors[:,1], Permeability_tensor


