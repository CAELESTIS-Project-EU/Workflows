
def writeAlyaPer(path, fileName, lmast):
    """
    Write Alya Periodicity file
    """
    fo = open(path+fileName+".per.dat","w", newline='\n')
    fo.write("LMAST\n")
    for i in range(len(lmast)):
        fo.write("{0} {1}\n".format(lmast[i][0],lmast[i][1]))
    fo.write("END_LMAST\n")
    fo.close()
