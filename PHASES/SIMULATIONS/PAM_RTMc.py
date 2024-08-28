# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 15:47:58 2023

@author: SMO
"""
import os
from PHASES.ESI.utils.bbesi_rtm_api import Visual_API
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.constraint import constraint
from pycompss.api.multinode import multinode
from PHASES.ESI.utils.lecture_erf import extract_num_step_filling
from PHASES.ESI.utils.write_file_ori import write_mapping
from PHASES.ESI.utils.write_file_ori import write_settemperature

import shutil


#@constraint(computing_units="PAM_NP")
@constraint(computing_units=16)
@multinode(computing_nodes=1)
@task(input_files_folder=DIRECTORY_IN, outputs_files_folder=DIRECTORY_OUT, source_folder=DIRECTORY_IN, src_macros_folder= DIRECTORY_IN, returns=1)
def run(RTM_base_name, Curing_base_name, input_files_folder, outputs_files_folder, source_folder, src_macros_folder, machine, DoE_line, np, **kwargs):
    print('_____________________________________________________________________________________')
    print('Starting curing simulation')
    
    #Visual will read the variables values from a txt file that is written at the end of this section
        

    if not os.path.exists(outputs_files_folder):
        os.makedirs(outputs_files_folder)
        print("Folder '{}' created.".format(outputs_files_folder))
    else:
        print("Folder '{}' already exists.".format(outputs_files_folder))


    
    mod_files_folder = os.path.join(outputs_files_folder, "mod_macros")
    os.makedirs(mod_files_folder)
    
    display = 1
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
        vsPath = 'gcc'
        RTMSolverPath = r'/gpfs/projects/bsce81/MN4/bsce81/esi/pamrtm/2022.5/Linux_x86_64_2.36/bin/pamcmxdmp.sh'
        RTMsolverVEPath = r'/gpfs/projects/bsce81/MN4/bsce81/esi/Visual-Environment/18.0/Linux_x86_64_2.17/VEBatch.sh'
    elif machine == 'JVNYDS':
        vsPath = r'C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvarsall.bat'
        RTMSolverPath = r'C:/Program Files/ESI Group/PAM-COMPOSITES/2022.0/RTMSolver\bin/pamcmxdmp.bat'
        if display == 1:
            RTMsolverVEPath = r'C:/Program Files/ESI Group/Visual-Environment/18.0/Windows-x64/VisualEnvironment.bat'
        else :
            RTMsolverVEPath = r'C:/Program Files/ESI Group/Visual-Environment/18.0/Windows-x64/VEBatch.bat'
    elif machine == 'JVNCFT':
        vsPath = r'C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvarsall.bat'
        RTMSolverPath = r'C:/Program Files/ESI Group/PAM-COMPOSITES/2022.0/RTMSolver\bin/pamcmxdmp.bat'
        if display == 1:
            RTMsolverVEPath = r'C:/Program Files/ESI Group/Visual-Environment/18.0/Windows-x64/VisualEnvironment.bat'
        else :
            RTMsolverVEPath = r'C:/Program Files/ESI Group/Visual-Environment/18.0/Windows-x64/VEBatch.bat'

    # Fixed variables
    SourceDirectory = source_folder
    VariablesTxtPath = os.path.abspath(os.path.join(os.getcwd(), 'VariablesList.txt'))
    RTMVdbName = RTM_base_name + '.vdb'
    VdbRTMFilePath = os.path.abspath(os.path.join(outputs_files_folder, RTMVdbName))
    CuringVdbName = Curing_base_name + '.vdb'
    RTMbasefolder = os.path.join(input_files_folder)
    Curingbasefolder = os.path.join(outputs_files_folder)
    SourceVdbCuringFilePath = os.path.join(SourceDirectory, CuringVdbName)
    
    VdbCuringFilePath = os.path.join(outputs_files_folder, CuringVdbName)
    RTMunfFile = RTM_base_name + 'g.unf'
    RTMerfh5File = RTM_base_name + '_RESULT.erfh5'
    RTMunfFilesPath = os.path.join(RTMbasefolder, RTMunfFile)
    RTMerfh5FilePath = os.path.join(RTMbasefolder, RTMerfh5File)

    CuringCATGENerfName = Curing_base_name + '_CATGEN.erfh5'
    CuringCATGENerfPath = os.path.join(Curingbasefolder, CuringCATGENerfName)

    resin_kinetics_init_path = os.path.join(SourceDirectory, Curing_base_name + '_resinkinetics.c')
    resin_kinetics_copy_path = os.path.join(outputs_files_folder, Curing_base_name + '_resinkinetics.c')
    pc_file_init_path = os.path.join(SourceDirectory, Curing_base_name + '.pc')
    pc_file_copy_path = os.path.join(outputs_files_folder, Curing_base_name + '.pc')


    if 'Mold_temperature' in DoE_line:
        if str(DoE_line['Mold_temperature']) != '-1':
            temp_mold_curing = DoE_line['Mold_temperature']
        else:
            temp_mold_curing = 'N/A'

    shutil.copy(resin_kinetics_init_path, resin_kinetics_copy_path)
    shutil.copy(pc_file_init_path, pc_file_copy_path)
    
    nb_step_filling = extract_num_step_filling(RTMerfh5FilePath)
    mapping_file_path = os.path.join(mod_files_folder, '22_CuringMappingTempFillFactCureDegree.py')
    write_mapping(mapping_file_path, nb_step_filling-2)

    temperature_file_path = os.path.join(source_folder, 'Temperature.txt')
    curing_set_temp_file_path = os.path.join(mod_files_folder, '23_CuringSetTemperature.py')
    write_settemperature(curing_set_temp_file_path, temperature_file_path,temp_mold_curing)

    MacroCuringList = [os.path.join(src_macros_folder, '21_SetCuringStrategy.py'),
                       mapping_file_path,
                       curing_set_temp_file_path,
                       os.path.join(src_macros_folder, '24_CuringWriteSolverInput.py')]


    
    # Internal info
    VariablesDict = {}
    VariablesDict['VdbRTMFilePath'] = VdbRTMFilePath
    VariablesDict['RTMsolverVEPath'] = RTMsolverVEPath
    VariablesDict['RTMSolverPath'] = RTMSolverPath
    VariablesDict['VdbCuringFilePath'] = VdbCuringFilePath
    VariablesDict['RTMunfFilePath'] = RTMunfFilesPath
    VariablesDict['CuringCATGENerfPath'] = CuringCATGENerfPath
    VariablesDict['outputs_files_folder'] = outputs_files_folder
    VariablesDict['vsPath'] = vsPath

    #Copy files to destination folder
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
   
    if 'Curing_cycle' in DoE_line:
            MacroCuringList.append(os.path.join(src_macros_folder,'23_CuringSetTemperature.py'))
            VariablesDict['Curing_cycle'] = DoE_line['Curing_cycle']

    # PAM-RTM uses its own python instance. A txt file is used to send it the required information
    f = open(os.path.join(VariablesTxtPath), "w+")
    for elem in VariablesDict:
        f.write(str(elem) + "= " + str(VariablesDict[elem]) + "\n")
    f.close()

    # Curing
    # Application initialization
    Curingmodel = Visual_API()
    Curingmodel.FileName = Curing_base_name
    Curingmodel.solverPath = RTMSolverPath
    Curingmodel.solverVEPath = RTMsolverVEPath
    Curingmodel.vsPath = vsPath
    Curingmodel.basefolder = Curingbasefolder
    Curingmodel.inputFile = VdbCuringFilePath
    Curingmodel.SourceFilesPath = SourceDirectory
    Curingmodel.VariablesTxtPath = VariablesTxtPath
    Curingmodel.simtype = 'CURING' #'RTM'
    Curingmodel.machine = machine
    OutputfileName = Curing_base_name + '.out'
    Curingmodel.machine = 'CLUSTER'
    Curingmodel.outputFile = os.path.join(Curingbasefolder, OutputfileName)
    Curingmodel.display = display
    Curingmodel.fp = 1 # Floating point precision (1: SP , 2: DP , note IMPLICIT requires DP)
    Curingmodel.nt = 2 # Number of threads
    Curingmodel.mp = 1 # 1 (default): SMP parallel mode; 2: DMP parallel mode
    Curingmodel.np = int(np) 
    Curingmodel.mpidir = None

    # JEA: Strange I think it is not necessary
    #Scriptsfolder = os.getcwd()
    #file_path =os.path.join(VariablesTxtPath)
    #shutil.copy(file_path, os.path.join(Scriptsfolder,'VariablesList.txt'))

    #Execute macros
    for elem in MacroCuringList:
        Curingmodel.LaunchMacro(elem)
    #solve
    
    Curingmodel.solveStep(runInBackground=False)

    return "PAM_RTMc finished"
