# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 15:47:58 2023

@author: SMO
"""
import os
from PHASES.AUTOMATION_ML.utils.bbesi_rtm_api import Visual_API
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(returns=1)
def run(RTM_base_name, Curing_base_name, **kwargs):
    import socket
    print('_____________________________________________________________________________________')
    print('Starting curing simulation')
    
    print(f"kwargs: {kwargs}")
    #%% Variables
    #Curing_base_name = 'Lk_Curing'
    #RTM_base_name = 'Lk_RTM_40'
    
    #Visual will read the variables values from a txt file that is written at the end of this section
    if "source_folder" in kwargs:
        source_folder_folder = kwargs["source_folder"]
        
    if "inputs_folder" in kwargs:
        input_files_folder = kwargs["inputs_folder"]
        #print('inputs folder is : ', input_files_folder)

    if "outputs_folder" in kwargs:
        outputs_files_folder = kwargs["outputs_folder"]
        if not os.path.exists(outputs_files_folder):
            os.makedirs(outputs_files_folder)
    
    if "machine" in kwargs:
        machine = kwargs["machine"]
    display = 0
    #paths
    if machine == 'BORLAP020':
        RTMSolverPath = r'C:\Program Files\ESI Group\PAM-COMPOSITES\2022.5\RTMSolver\bin\pamcmxdmp.bat'
        if display == 1:
            RTMsolverVEPath = r'C:\Program Files\ESI Group\Visual-Environment\18.0\Windows-x64\VisualEnvironment.bat'
        else :
            RTMsolverVEPath = r'C:\Program Files\ESI Group\Visual-Environment\18.0\Windows-x64\VEBatch.bat'
    elif machine == 'bruclu':
        display = 0
        RTMSolverPath = r'/nisprod/ppghome/ppg/dist/pamcmx/2022.5/Linux_x86_64_2.17/bin/pamcmxdmp.sh'
        RTMsolverVEPath = r'/nisprod/ppghome/ppg/dist/Visual-Environment/18.0/Linux_x86_64_2.17/VEBatch.sh'
    elif machine == 'HPCBSC':
        display = 0
        RTMSolverPath = r'/gpfs/projects/bsce81/esi/pamrtm/2022.5/Linux_x86_64_2.36/bin/pamcmxdmp.sh'
        RTMsolverVEPath = r'/gpfs/projects/bsce81/esi/Visual-Environment/18.0/Linux_x86_64_2.17/VEBatch.sh'

    # Fixed variables
    SourceDirectory = source_folder_folder
    VariablesTxtPath = os.path.abspath(os.path.join(SourceDirectory, 'VariablesList.txt'))
    RTMVdbName = RTM_base_name + '.vdb'
    VdbRTMFilePath = os.path.abspath(os.path.join(outputs_files_folder, RTMVdbName))
    CuringVdbName = Curing_base_name + '.vdb'
    RTMbasefolder = os.path.join(input_files_folder)
    Curingbasefolder = os.path.join(outputs_files_folder)
    SourceVdbCuringFilePath = os.path.join(SourceDirectory, CuringVdbName)
    
    VdbCuringFilePath = os.path.join(outputs_files_folder, CuringVdbName)
    RTMunfFile = RTM_base_name + 'g.unf'
    RTMunfFilesPath = os.path.join(RTMbasefolder, RTMunfFile)
    CuringCATGENerfName = Curing_base_name + '_CATGEN.erfh5'
    CuringCATGENerfPath = os.path.join(Curingbasefolder, CuringCATGENerfName)

    MacroCuringList = ['22_CuringMappingTempFillFactCureDegree.py',
                       '23_CuringSetTemperature.py',
                       '24_CuringWriteSolverInput.py']
    
    # Internal info
    VariablesDict = {}
    VariablesDict['VdbRTMFilePath'] = VdbRTMFilePath
    VariablesDict['RTMsolverVEPath'] = RTMsolverVEPath
    VariablesDict['RTMSolverPath'] = RTMSolverPath
    VariablesDict['VdbCuringFilePath'] = VdbCuringFilePath
    VariablesDict['RTMunfFilePath'] = RTMunfFilesPath
    VariablesDict['CuringCATGENerfPath'] = CuringCATGENerfPath
    VariablesDict['outputs_files_folder'] = outputs_files_folder

    #Copy files to destination folder
    import shutil
    try:
        shutil.copy(SourceVdbCuringFilePath, outputs_files_folder)
        #print('File ' + SourceVdbCuringFilePath + ' copied to ' + outputs_files_folder)
    except:
        print('Vdb Curing file path is not at:')
        print('     ', SourceVdbCuringFilePath)
    # Default values
    VariablesDict['Viscosity'] = 0.2

    # Read Doe
    Curing_parameters_list = ['Curing_cycle']
    
    # Modified values
    if "DoE_line" in kwargs:
        if 'Curing_cycle' in kwargs['DoE_line']:
            MacroCuringList.append('23_CuringSetTemperature.py')
            VariablesDict['Curing_cycle'] = kwargs['DoE_line']['Curing_cycle']

    # PAM-RTM uses its own python instance. A txt file is used to send it the required information
    f = open(os.path.join(VariablesTxtPath), "w+")
    for elem in VariablesDict:
        f.write(str(elem) + "= " + str(VariablesDict[elem]) + "\n")
    f.close()

#%% Curing
    # Application initialization
    Curingmodel = Visual_API()
    Curingmodel.FileName = Curing_base_name
    Curingmodel.solverPath = RTMSolverPath
    Curingmodel.solverVEPath = RTMsolverVEPath
    Curingmodel.basefolder = Curingbasefolder
    Curingmodel.inputFile = VdbCuringFilePath
    Curingmodel.SourceFilesPath = SourceDirectory
    Curingmodel.VariablesTxtPath = VariablesTxtPath
    Curingmodel.simtype = 'RTM'
    Curingmodel.machine = machine
    OutputfileName = Curing_base_name + '.out'
    Curingmodel.machine = 'CLUSTER'
    Curingmodel.outputFile = os.path.join(Curingbasefolder, OutputfileName)
    Curingmodel.display = display
    Curingmodel.fp = 1 # Floating point precision (1: SP , 2: DP , note IMPLICIT requires DP)
    Curingmodel.nt = 2 # Number of threads
    Curingmodel.mp = 1 # 1 (default): SMP parallel mode; 2: DMP parallel mode

    #Execute macros
    for elem in MacroCuringList:
        Curingmodel.LaunchMacro(elem)
    #solve
    
    Curingmodel.solveStep(runInBackground=False)

    return
