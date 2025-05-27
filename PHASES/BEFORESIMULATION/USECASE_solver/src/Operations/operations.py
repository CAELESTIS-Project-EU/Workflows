import numpy as np
import shutil
from pathlib import Path

def dos2unix(input_file, output_file):
    """
    Files in UNIX format
    """
    with open(input_file, 'r', newline='') as dos_file:
        content = dos_file.read()

    with open(output_file, 'w', newline='\n') as unix_file:
        unix_file.write(content)

def copyTemplatefile(src_path, dest_dir, new_name):
    """
    Copy a file from src_path to dest_dir and rename it to new_name.
    
    Args:
        src_path (str or Path): The path of the source file to copy.
        dest_dir (str or Path): The destination directory where the file should be copied.
        new_name (str): The new name for the copied file.
    """
    # Ensure paths are Path objects
    src_path = Path(src_path)
    dest_dir = Path(dest_dir)
    # Make sure the destination directory exists
    dest_dir.mkdir(parents=True, exist_ok=True)
    # Define the destination path with the new file name
    dest_path = dest_dir / new_name
    # Copy the file to the destination and rename it
    shutil.copy(src_path, dest_path)
    
    return

def operateExternalFile(dataList, VERBOSE):
    """
    Operate with external file
    """
    if VERBOSE:
        print('Operate with external file ...')

    EleList, VfList, thList, v1List, v2List, v3List  = [], [], [], [], [], []
    ielem = 0
    for i in range(len(dataList)):
        ielem += 1
        thList.append(dataList[i][1])
        v1List.append(dataList[i][6:9])
        v2List.append(dataList[i][9:])
        v3 = list(np.cross(np.array(dataList[i][6:9]), np.array(dataList[i][9:])))
        v3List.append(v3)
        EleList.append(dataList[i][0])
        VfList.append(dataList[i][2])
        
    return EleList, VfList, thList, v1List, v2List, v3List

def operateMeshNoCoh(npart, nList, eList, pList, layup, VERBOSE):
    """
    Operate with Abaqus mesh without cohesive elements
    """
    if VERBOSE:
        print('Operate with Abaqus mesh without cohesive elements ...')

    # Sort nodal coordinates
    nList = list(set(map(tuple, nList)))
    nListNew = sorted(nList, key=lambda nList_entry: nList_entry[0])

    # Element ranges for each part
    nelemCounter = [[0, pList[0][2]],]
    ielem = pList[0][2]
    for j in range(len(pList)-1):
        ielem += pList[j+1][2]
        nelemCounter.append([nelemCounter[j][1], ielem])

    # Build nodal coordinates, element connectivities, material list, set list and ori list
    eListNew = []
    mList, sList, oList  = [], [], []
    ipart = 0
    ielem = 0
    for i in range(npart):
        ipart += 1
        eListPart = eList[nelemCounter[i][0]:nelemCounter[i][1]]
        ori = layup[i]
        for j in range(len(eListPart)):
            ielem += 1
            eListNew.append([ielem]+eListPart[j][1:])
            # Materials and sets
            mList.append([ielem,ipart])
            sList.append([ielem,ipart])
            oList.append([ielem,ori])

    return nListNew, eListNew, mList, oList, sList

def operateMeshCoh(npart, nList, eList, pList, layup, VERBOSE):
    """
    Operate with Abaqus mesh with cohesive elements
    """
    if VERBOSE:
        print('Operate with Abaqus mesh with cohesive elements ...')

    # Node and Element ranges for each part
    npoinCounter = [[0, pList[0][1]],]
    nelemCounter = [[0, pList[0][2]],]
    ipoin = pList[0][1]
    ielem = pList[0][2]
    for j in range(len(pList)-1):
        ipoin += pList[j+1][1]
        ielem += pList[j+1][2]
        npoinCounter.append([npoinCounter[j][1], ipoin])
        nelemCounter.append([nelemCounter[j][1], ielem])
        
    nListNew, eListNew = [], []
    mList, sList, oList, cList = [], [], [], []
    ipart = 0
    ielem = 0
    inode = 0
    for i in range(npart):
        nodes_part_new = []
        ipart += 1
        ori = layup[i]

        nListPart = nList[npoinCounter[i][0]:npoinCounter[i][1]]
        eListPart = eList[nelemCounter[i][0]:nelemCounter[i][1]]
        
        nListPart      = sorted(nListPart, key=lambda nListPart_entry: nListPart_entry[0])
        nodes_part_old = [ nListPart[i][0] for i in range(len(nListPart))]
        
        # Renumbering (Nodes)
        for i in range(len(nListPart)):
            inode += 1
            nListNew.append([inode]+nListPart[i][1:])
            nodes_part_new.append(inode)
            
        # Renumbering (Element connectivities) 
        for j in range(len(eListPart)):
            ielem += 1
            elcon_old = eListPart[j][1:]
            elcon_new = [ielem]
            for jnode in elcon_old:
                ipos = nodes_part_old.index(jnode)
                elcon_new += [nodes_part_new[ipos]]
            eListNew.append(elcon_new)
            # Materials, Characteristics and Sets
            mList.append([ielem]+[ipart])
            oList.append([ielem]+[ori])
            sList.append([ielem]+[ipart])
            cList.append([ielem]+[0])

    # Adding cohesive elements
    ipart = 0
    elTopBulkList, elBotBulkList = [], []
    for i in range(npart):
        ipart += 1
        eListPart = eList[nelemCounter[i][0]:nelemCounter[i][1]]
       #eListPart = sorted(eListPart, key=lambda eListPart_entry: eListPart_entry[0]) #not sure

        if i != (npart-1):
            for k in range(len(eListPart)):
                eltopBulk_con = eListPart[k][5:9]
                elTopBulkList.append(eltopBulk_con)
        if i != 0:
            for k in range(len(eListPart)):
                elbotBulk_con = eListPart[k][1:5]
                elBotBulkList.append(elbotBulk_con)

    ielem = len(eListNew)
    icode_mat = npart + 1
    for icoh in range(len(elTopBulkList)):
        ielem += 1 
        eListNew.append([ielem] + elTopBulkList[icoh][:] + elBotBulkList[icoh][:])
        mList.append([ielem]+[icode_mat])
        sList.append([ielem]+[0])
        cList.append([ielem]+[7])
   
    return nListNew, eListNew, mList, sList, oList, cList
