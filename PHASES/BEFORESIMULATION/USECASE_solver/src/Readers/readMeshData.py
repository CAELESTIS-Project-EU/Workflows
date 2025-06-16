VERBOSITY = 0

def verbosityPrint(VERBOSE,str):
    if VERBOSE:
        print(str)
    else:
        pass
  
def readlperm(lpermFile,VERBOSE):
    """
    Read data file
    Element_ID Thickness Fiber_Content K1 K2 K3 Perm_Vec1_x Perm_Vec1_y Perm_Vec1_z Perm_Vec2_x Perm_Vec2_y Perm_Vec2_z
    """
    f = open(lpermFile,'r')
    dataList = []
    line = True
    while line:
        line = f.readline()
        if line == '':
            verbosityPrint(VERBOSE,'End of file')
            line = False
        else:
            if '#' in line:
                verbosityPrint(VERBOSE,'Header')
                line = True
            else:
                stripline = line.strip().split()
                elementLine = []
                for i in range(len(stripline)):
                    if i == 0:
                        ivalue = int(stripline[i])
                    else:
                        ivalue = float(stripline[i])
                    elementLine.append(ivalue)
                dataList.append(elementLine)
                line = True
    f.close()

    return dataList
    
def readAbaqusParts(inpFile,VERBOSE):
    """
    Read coordinates and element connectivities for each Abaqus *Part
    """
    f = open(inpFile,'r')
    eList, nList, sList, pList = [], [], [], [] 
    line = True
    inNode = False
    inElem = False
    ipart = 0
    while line:
        line = f.readline()
        if line == '':
            verbosityPrint(VERBOSE,'End of file')
            line = False
        else:
            if '*Part' in line:
                ipart += 1
                ielem = 0
                inode = 0
                if VERBOSE:
                    print('Part No.',ipart)
                
            elif '*Node' in line:
                verbosityPrint(VERBOSE,'Reading *Node section ...')
                if '*Element' in line:
                    verbosityPrint(VERBOSE,'Finished *Node section')
                    inNODE = False
                    line = True
                else:
                    inNode = True
                    line = True
            elif '*Element' in line:
                verbosityPrint(VERBOSE,'Reading *Element section ...')
                if '*Node' in line:
                    verbosityPrint(VERBOSE,'Finished *Element section')
                    inElem = False
                    line = True
                else:
                    inElem = True
                    line = True
            elif '*End Part' in line:
                inNode = False
                inElem = False
                pList.append([ipart, inode, ielem])
                if VERBOSE:
                    print('  Nodes:', inode)
                    print('  Elements:', ielem)
            elif '**' in line:
                inNode = False
                inElem = False
            else:
                if inElem:
                    ielem += 1
                    stripline = line.strip().replace(',',' ').split()
                    s = [int(i) for i in stripline]
                    eList.append(s)
                    # Part list (set)
                    sList.append([stripline[0], ipart])
                    line = True
                elif inNode:
                    inode += 1
                    stripline = line.strip().replace(',',' ').split()
                    nodeLine = []
                    for i in range(len(stripline)):
                        if i == 0:
                            ivalue = int(stripline[i])
                        else:
                            ivalue = float(stripline[i])
                        nodeLine.append(ivalue)
                    nList.append(nodeLine)
                    line = True
                else:
                    line = True
    f.close()

    npart = ipart
    
    return npart, nList, eList, sList, pList
