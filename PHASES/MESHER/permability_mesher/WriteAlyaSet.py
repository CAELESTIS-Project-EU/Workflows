
def writeAlyaSet(path, fileName, nelem, nboun):
    """ Alya caseName.set.dat file
    """

    stream = open(path+fileName+'.set.dat', 'w', newline='\n')

    stream.write("ELEMENTS\n")
    for i in range(0,nelem):
        stream.write(f'{i+1} {1}\n')   
    stream.write("END_ELEMENTS\n")

    stream.write("BOUNDARIES\n")
    stream.write("END_BOUNDARIES\n")
    
    
