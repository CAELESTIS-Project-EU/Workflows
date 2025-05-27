def writeAlyaCooDat(fileName,nList):
    """
    Write Alya coo.dat file
    """
    with open(fileName, 'w') as stream:
        stream.write('COORDINATES\n')
        for i in range(len(nList)):
            stream.write(f'{nList[i][0]} {nList[i][1]}  {nList[i][2]}  {nList[i][3]} \n')
        stream.write('END_COORDINATES\n')
    stream.close()

def writeAlyaEleDat(fileName,eList):
    """
    Write Alya ele.dat file
    """
    with open(fileName, 'w') as stream:
        stream.write('ELEMENTS\n')
        for i in range(len(eList)):
            if len(eList[i][:]) == 9:   # HEX08
                stream.write(f'{eList[i][0]} {eList[i][1]} {eList[i][2]} {eList[i][3]} {eList[i][4]} {eList[i][5]} {eList[i][6]} {eList[i][7]} {eList[i][8]}\n')
            elif len(eList[i][:]) == 7: # PEN06
                stream.write(f'{eList[i][0]} {eList[i][1]} {eList[i][2]} {eList[i][3]} {eList[i][4]} {eList[i][5]} {eList[i][6]}\n')
            else:
                print('Error: element type not parsed!')
                        
        stream.write('END_ELEMENTS\n')
    stream.close()

def writeAlyaNpeDat(fileName,eList):
    """
    Write Alya npe.dat file
    """
    with open(fileName, 'w') as stream:
        stream.write('NODES_PER_ELEMENT\n')
        for i in range(len(eList)):
            stream.write(f'{eList[i][0]} {len(eList[i][1:])}\n')
        stream.write('END_NODES_PER_ELEMENT\n')
    stream.close()
    
def writeAlyaSetDat(fileName,sList):
    """
    Write Alya set.dat file
    """
    with open(fileName, 'w') as stream:
        stream.write('ELEMENTS\n')
        for i in range(len(sList)):
            stream.write(f'{sList[i][0]} {sList[i][1]}\n')
        stream.write('END_ELEMENTS\n')
    stream.close()
    
def writeAlyaChaDat(fileName, cList):
    """
    Write Alya cha.dat file
    """
    with open(fileName, 'w') as stream:
        stream.write('CHARACTERISTICS\n')
        for i in range(len(cList)):
            stream.write(f'{cList[i][0]} {cList[i][1]}\n')
        stream.write('END_CHARACTERISTICS\n')
    stream.close()
    
def writeAlyaMatDat(fileName, mList):
    """
    Write Alya mat.dat file
    """
    with open(fileName, 'w') as stream:
        stream.write('MATERIALS\n')
        for i in range(len(mList)):
            stream.write(f'{mList[i][0]} {mList[i][1]}\n')
        stream.write('END_MATERIALS\n')
    stream.close()

def writeAlyaFieDat(fileName, kfl_ori, eList, oList, v1List, v2List, v3List):
    """
    Write Alya fie.dat file
    """
    if kfl_ori== 'lperm':
        
        with open(fileName, 'w') as stream:
            stream.write('FIELD= 1\n')
            for i in range(len(eList)):
                try:
                    stream.write(f'{eList[i][0]} {v1List[i][0]} {v1List[i][1]} {v1List[i][2]} {v2List[i][0]} {v2List[i][1]} {v2List[i][2]} {v3List[i][0]} {v3List[i][1]} {v3List[i][2]}\n')
                except:
                    stream.write(f'{eList[i][0]} {1.0} {0.0} {0.0} {0.0} {1.0} {0.0} {0.0} {0.0} {1.0}\n')
            
            stream.write('END_FIELD\n')
        stream.close()

    elif kfl_ori == 'uniform':
    
        with open(fileName, 'w') as stream:
            stream.write('FIELD= 1\n')
            for i in range(len(eList)):
                try:
                    stream.write(f'{eList[i][0]} {oList[i][1]}\n')
                except:
                    stream.write(f'{eList[i][0]} {0.0}\n')
                
            stream.write('END_FIELD\n')
        stream.close()
