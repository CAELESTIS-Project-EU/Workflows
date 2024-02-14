
def writeAlyaMat(path ,fileName, Elementsetmaterials):
    """ Alya caseName.mat.dat file
    """
    nmate = 2 # TODO: Lo tenemos harcodeado
    
    stream = open(path + fileName + '.mat.dat',"w", newline='\n')
    
    stream.write("MATERIALS\n")

    for i in range(len(Elementsetmaterials)):
        elementId = int(Elementsetmaterials[i][0])
        materialId = int(Elementsetmaterials[i][1])
        if materialId == 2:
            # Bulk
            stream.write(f'{i+1} {1}\n')
        else:
            # Gap
            stream.write(f'{i+1} {2}\n')
        
    stream.write("END_MATERIALS\n")
    
    stream.close()
    
    return nmate
