# -*- coding: utf-8 -*-
"""
ESI Group
SMO
"""
import os
import socket
from bbesi_rtm_api import Visual_API
def PAM_DISTORTION(**kwargs):
    
    # import socket
    # Variables
    # Visual will read the variables values from a txt file that is written at the end of this section
    print('_____________________________________________________________________________________')
    print('Starting distortion simulation')
    if "source_folder" in kwargs:
        source_folder_folder = kwargs["source_folder"]
        
    if "inputs_folder" in kwargs:
        input_files_folder = kwargs["inputs_folder"]
    if "outputs_folder" in kwargs:
        outputs_files_folder = kwargs["outputs_folder"]
        if not os.path.exists(outputs_files_folder):
            os.makedirs(outputs_files_folder)
            print("Folder '{}' created.".format(outputs_files_folder))
        else:
            print("Folder '{}' already exists.".format(outputs_files_folder))
    else:
        print('no outputs file provided!!!')

    Distortion_Base_Name = 'Lk_Distortion_40'
    Curing_base_name = 'Lk_Curing'
    
    if "machine" in kwargs:
        machine = kwargs["machine"]
        
    if "gaps" in kwargs:
        gaps = kwargs["gaps"]
            
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
        DistortionSolverFolderPath = r'/gpfs/projects/bsce81/esi/pamdistortion/2022.5/Linux_x86_64/bin'
        DistortionSolverFilePath = r'/gpfs/projects/bsce81/esi/pamdistortion/2022.5/Linux_x86_64/bin/pamdistortion'
        DistortionsolverVEPath = r'/gpfs/projects/bsce81/esi/Visual-Environment/18.0/Linux_x86_64_2.17/VEBatch.sh'
        DistortionsolverWinTailPath = r"C:\Program Files\ESI Group\PAM-COMPOSITES\2022.5\Solver\bin\WinTail.exe"

    # Fixed variables
    SourceDirectory = source_folder_folder
    VariablesTxtPath = os.path.join(SourceDirectory, 'VariablesList.txt')
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

    import shutil
    shutil.copy(SourceVdbDistortionFilePath, outputs_files_folder)

    MacroDistortionList = [#'31_DistortionPreparingModel.py',
                          #'32_DistortionResinParameters.py',
                         #'33_DistortionFiberParameters.py',
                         #'34_DistortionComputePly.py',
                         #'35_DistortionCharacterizeLaminate.py',
                         '36_DistortionProcessConditions.py',
                         '37_DistortionSimulationParameters.py'
                         ]
    
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

    #Application initialization
    Distortionmodel = Visual_API()
    Distortionmodel.FileName = Distortion_Base_Name
    Distortionmodel.solverPath = DistortionSolverFilePath
    Distortionmodel.solverVEPath = DistortionsolverVEPath
    Distortionmodel.basefolder = Distortionbasefolder
    Distortionmodel.inputFile = PcDistortionFilePath
    Distortionmodel.SourceFilesPath = SourceDirectory
    Distortionmodel.VariablesTxtPath = VariablesTxtPath

    if machine == 'BORLAP020':
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
    
    # #Execute macros
    for elem in MacroDistortionList:
          Distortionmodel.LaunchMacro(elem)
    
    Distortionmodel.LaunchMacro('38_DistortionRun.py')
    
    # solve
    Distortionmodel.solveStep(runInBackground=False)

    return

