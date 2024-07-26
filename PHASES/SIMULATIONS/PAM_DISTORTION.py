# -*- coding: utf-8 -*-
"""
ESI Group
SMO
"""
import os
import shutil
from PHASES.AUTOMATION_ML.utils.bbesi_rtm_api import Visual_API
from PHASES.ESI.utils.write_file_ori import write_ori_dist
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.constraint import constraint
from pycompss.api.multinode import multinode

#@constraint(computing_units="PAM_NP")
@constraint(computing_units=16)
@multinode(computing_nodes=1)
@task(input_files_folder=DIRECTORY_IN, outputs_files_folder=DIRECTORY_OUT, source_folder=DIRECTORY_IN, src_macros_folder=DIRECTORY_IN, returns=1)
def run(Curing_base_name, Distortion_Base_Name, input_files_folder, outputs_files_folder, source_folder, src_macros_folder, machine, DoE_line, np, **kwargs):
    # import socket
    # Variables
    # Visual will read the variables values from a txt file that is written at the end of this section
    print('_____________________________________________________________________________________')
    print('Starting distortion simulation')
        

    if not os.path.exists(outputs_files_folder):
        os.makedirs(outputs_files_folder)
        print("Folder '{}' created.".format(outputs_files_folder))
    else:
        print("Folder '{}' already exists.".format(outputs_files_folder))

    mod_files_folder = os.path.join(outputs_files_folder, "mod_macros")
    os.makedirs(mod_files_folder)
           
    display = 0
    # paths
    if machine == 'BORLAP020':
        DistortionSolverFolderPath = r'C:\Program Files\ESI Group\PAM-COMPOSITES\2022.5\Solver\bin'
        DistortionSolverFilePath = r'C:\Program Files\ESI Group\PAM-COMPOSITES\2022.5\Solver\bin\pamdistortion.bat'
        if display == 1:
            DistortionsolverVEPath = r'C:\Program Files\ESI Group\Visual-Environment\18.0\Windows-x64\VisualEnvironment.bat'
        else:   
            DistortionsolverVEPath = r'C:\Program Files\ESI Group\Visual-Environment\18.0\Windows-x64\VEBatch.bat'
        DistortionsolverWinTailPath = r"C:\Program Files\ESI Group\PAM-COMPOSITES\2022.5\Solver\bin\WinTail.exe"
    elif machine == 'bruclu':
        display = 0
        DistortionSolverFolderPath = r'/nisprod/ppghome/ppg/dist/pamdistortion/2022.5/Linux_x86_64/bin'
        DistortionSolverFilePath = r'/nisprod/ppghome/ppg/dist/pamdistortion/2022.5/Linux_x86_64/bin/pamdistortion'
        DistortionsolverVEPath = r'/nisprod/ppghome/ppg/dist/Visual-Environment/18.0/Linux_x86_64_2.17/VEBatch.sh'
        DistortionsolverWinTailPath = r"C:\Program Files\ESI Group\PAM-COMPOSITES\2022.5\Solver\bin\WinTail.exe"
    elif machine == 'HPCBSC':
        display = 0
        DistortionSolverFolderPath = r'/gpfs/projects/bsce81/MN4/bsce81/esi/pamdistortion/2022.5/Linux_x86_64/bin'
        DistortionSolverFilePath = r'/gpfs/projects/bsce81/MN4/bsce81/esi/pamdistortion/2022.5/Linux_x86_64/bin/pamdistortion'
        DistortionsolverVEPath = r'/gpfs/projects/bsce81/MN4/bsce81/esi/Visual-Environment/18.0/Linux_x86_64_2.17/VEBatch.sh'
        DistortionsolverWinTailPath = r"C:\Program Files\ESI Group\PAM-COMPOSITES\2022.5\Solver\bin\WinTail.exe"
    elif machine == 'JVNYDS':
        DistortionSolverFolderPath = r'C:\Program Files\ESI Group\PAM-COMPOSITES\2022.0\Solver\bin'
        DistortionSolverFilePath = r'C:\Program Files\ESI Group\PAM-COMPOSITES\2022.0\Solver\bin\pamdistortion.bat'
        if display == 1:
            DistortionsolverVEPath = r'C:\Program Files\ESI Group\Visual-Environment\18.0\Windows-x64\VisualEnvironment.bat'
        else:
            DistortionsolverVEPath = r'C:\Program Files\ESI Group\Visual-Environment\18.0\Windows-x64\VEBatch.bat'
        DistortionsolverWinTailPath = r"C:\Program Files\ESI Group\PAM-COMPOSITES\2022.0\Solver\bin\WinTail.exe"
    elif machine == 'JVNCFT':
        DistortionSolverFolderPath = r'C:\Program Files\ESI Group\PAM-COMPOSITES\2022.0\Solver\bin'
        DistortionSolverFilePath = r'C:\Program Files\ESI Group\PAM-COMPOSITES\2022.0\Solver\bin\pamdistortion.bat'
        if display == 1:
            DistortionsolverVEPath = r'C:\Program Files\ESI Group\Visual-Environment\18.0\Windows-x64\VisualEnvironment.bat'
        else:
            DistortionsolverVEPath = r'C:\Program Files\ESI Group\Visual-Environment\18.0\Windows-x64\VEBatch.bat'
        DistortionsolverWinTailPath = r"C:\Program Files\ESI Group\PAM-COMPOSITES\2022.0\Solver\bin\WinTail.exe"

    # Fixed variables
    SourceDirectory = source_folder
    VariablesTxtPath = os.path.join(os.getcwd(), 'VariablesList.txt')
    CuringVdbName = Curing_base_name + '.vdb'
    DistortionVdbName = Distortion_Base_Name + '.vdb'
    DistortionPcName = Distortion_Base_Name + '.pc'
    DistortionIncName = Distortion_Base_Name + '.inc'
    DistortionOriName = Distortion_Base_Name + '.ori'
    Curingbasefolder = input_files_folder
    Distortionbasefolder = outputs_files_folder

    VdbCuringFilePath = os.path.join(Curingbasefolder, CuringVdbName)
    CuringCATGENerfName = Curing_base_name + '_CATGEN.erfh5'
    CuringCATGENerfPath = os.path.join(Curingbasefolder, CuringCATGENerfName)
    SourceVdbDistortionFilePath = os.path.join(SourceDirectory, DistortionVdbName)
    sourcePcDistortionFilePath = os.path.join(SourceDirectory, DistortionPcName)
    sourceIncDistortionFilePath = os.path.join(SourceDirectory, DistortionIncName)
    sourceOriDistortionFilePath = os.path.join(SourceDirectory, DistortionOriName)

    VdbDistortionFilePath = os.path.join(Distortionbasefolder, DistortionVdbName)
    PcDistortionFilePath = os.path.join(Distortionbasefolder, DistortionPcName)

    shutil.copy(SourceVdbDistortionFilePath, outputs_files_folder)

    VariablesDict = {}
    MacroDistortionList = []

    
    #%% Start running the DoE
    #write for macros
    VariablesDict = {}
    VariablesDict['VdbCuringFilePath'] = VdbCuringFilePath
    VariablesDict['VdbDistortionFilePath'] = VdbDistortionFilePath
    VariablesDict['SourceFilesPath'] = SourceDirectory
    VariablesDict['DistortionSolverFolderPath'] = DistortionSolverFolderPath
    VariablesDict['DistortionSolverFilePath'] = DistortionSolverFilePath
    VariablesDict['CuringCATGENerfPath'] = CuringCATGENerfPath
    VariablesDict['outputs_files_folder'] = outputs_files_folder
    
    # Default values
    VariablesDict['Viscosity'] = 0.2

    # Write the variables in a txt file.
    f = open(os.path.join(VariablesTxtPath), "w+")
    for elem in VariablesDict:
        f.write(str(elem) + "= " + str(VariablesDict[elem]) + "\n")
    f.close()

    if 'Orientation' in DoE_line:
        if str(DoE_line['Orientation']) != '-1':
            ori_file_path = os.path.join(mod_files_folder, '37_DISTMApplyOrientation.py')
            write_ori_dist(ori_file_path)
            MacroDistortionList.append(ori_file_path)
            VariablesDict['Orientation'] = DoE_line['Orientation']

    MacroDistortionList.append(src_macros_folder + '/' + '37_DistortionSimulationParameters.py')

    #Application initialization
    Distortionmodel = Visual_API()
    Distortionmodel.FileName = Distortion_Base_Name
    Distortionmodel.solverPath = DistortionSolverFilePath
    Distortionmodel.solverVEPath = DistortionsolverVEPath
    Distortionmodel.basefolder = Distortionbasefolder
    Distortionmodel.inputFile = PcDistortionFilePath
    Distortionmodel.SourceFilesPath = SourceDirectory
    Distortionmodel.VariablesTxtPath = VariablesTxtPath

    if machine == 'BORLAP020'or machine == 'JVNYDS' or machine == 'JVNCFT':
        BatFileName = Distortion_Base_Name + '.bat'
    else:
        BatFileName = Distortion_Base_Name + '.sh'
    Distortionmodel.BatFilePath = os.path.join(Distortionbasefolder, BatFileName)
    Distortionmodel.DistortionsolverWinTailPath = DistortionsolverWinTailPath
    Distortionmodel.simtype = 'DISTORTION'
    Distortionmodel.machine = machine
    OutputfileName = Distortion_Base_Name + '.out'
    Distortionmodel.outputFile = os.path.join(Distortionbasefolder, OutputfileName)
    Distortionmodel.display = display
    Distortionmodel.fp = 1 # Floating point precision (1: SP , 2: DP , note IMPLICIT requires DP)
    Distortionmodel.nt = 2 # Number of threads
    Distortionmodel.mp = 1 # 1 (default): SMP parallel mode; 2: DMP parallel mode
    Distortionmodel.np = int(np)
    Distorsionmodel.mpidir = None
    # #Execute macros
    for elem in MacroDistortionList:
          Distortionmodel.LaunchMacro(elem)
    
    Distortionmodel.LaunchMacro(os.path.join(src_macros_folder,'38_DistortionRun.py'))
    
    # solve
    Distortionmodel.solveStep(runInBackground=False)
    tools = False
    if tools == True:
        MacroUnmoldingList = []
        MacroUnmoldingList.append(os.path.join(src_macros_folder,'66_Distortion_unmolding.py'))
        MacroUnmoldingList.append(os.path.join(src_macros_folder,'38_DistortionRun.py'))
        for elem in MacroUnmoldingList:
            Distortionmodel.LaunchMacro(elem)

        # solve
        Distortionmodel.solveStep(runInBackground=False)

    return "PAM_DISTORSION finished"

