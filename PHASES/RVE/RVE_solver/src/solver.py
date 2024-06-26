import time

from .Readers.ReadAlyaMat import readAlyaMat
from .Readers.ReadAlyaCha import readAlyaCha
from .Readers.ReadAlyaGeo import readAlyaGeo

from .Writers.WriteAlyaDat import writeAlyaDat
from .Writers.WriteAlyaKer import writeAlyaKer
from .Writers.WriteAlyaDom import writeAlyaDom
from .Writers.WriteAlyaSld import writeAlyaSld3D
from .Writers.WriteAlyaSld import writeAlyaSld2D
from .Writers.WriteAlyaPos import writeAlyaPos

import numpy
import os
from pycompss.api.task import task
from pycompss.api.parameter import *

VERBOSITY = 1

if VERBOSITY == 1:
    def verbosityPrint(str):
        print(str)
else:
    def verbosityPrint(str):
        pass


def run(file, meshPath, outputPath, iload, debug):
    """
    Alya writer files
    """
    
    verbosityPrint('Writing Alya configuration files...')
    
    dash_iload = '-'+iload    
    writeAlyaDat(f'{outputPath}{file}{dash_iload}.dat', file, dash_iload, debug)
    writeAlyaKer(f'{outputPath}{file}{dash_iload}.ker.dat', iload, debug)
    if debug:
        writeAlyaPos(f'{outputPath}{file}{dash_iload}.post.alyadat')
    
    nOfMaterials = readAlyaMat(f'{meshPath}{file}.mat.dat')

    kfl_coh = False
    if os.path.exists(f'{meshPath}{file}.cha.dat'):
        kfl_coh = readAlyaCha(f'{meshPath}{file}.cha.dat')

    dim, lx, ly, lz = readAlyaGeo(f'{meshPath}{file}.geo.dat')
        
    writeAlyaDom(f'{outputPath}{file}{dash_iload}.dom.dat', file, dim, nOfMaterials, kfl_coh)

    if dim == 2:
        writeAlyaSld2D(f'{outputPath}{file}{dash_iload}.sld.dat', file, dash_iload, 'STATIC', kfl_coh, nOfMaterials, iload, lx, ly, lz, debug)
    else:
        writeAlyaSld3D(f'{outputPath}{file}{dash_iload}.sld.dat', file, dash_iload, 'STATIC', kfl_coh, nOfMaterials, iload, lx, ly, lz, debug)
    return

@task(returns=1)
def start(listloads, case, simulation_wdir, debug, **kwargs):
    # Get the start time
    st = time.time()

    #-------------------------------------------------------------------
    # User inputs
    #-------------------------------------------------------------------
    #case = 'RVE_10_10_1'
    #case = 'RVE_Test_1'
    #case = 'twoFibres'
    #case = 'oneFibre'
    #-------------------------------------------------------------------


    # Create load case scenarios    
    for iload in listloads:
        meshPath =  f'{simulation_wdir}/msh/'
        outputPath = f'{simulation_wdir}/'+case+'-'+str(iload)+'/'
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
            
        # Run Alya writer
        run(case, meshPath, outputPath, str(iload), debug)

    # Get the end time
    et = time.time()

    # Get the execution time
    elapsed_time = et - st
    
    if VERBOSITY == 1:
        print('Execution time:', round(elapsed_time,2), 'seconds')
    return True