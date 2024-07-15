"""
ESI Group
SMO
"""
import os
from PHASES.AUTOMATION_ML.utils.bbesi_rtm_api import Visual_API
from pycompss.api.task import task
from pycompss.api.parameter import *

@task(DoE_line=COLLECTION_IN,returns=1)
def run(RTM_base_name, **kwargs):
    '''
    This function assumes that parameter names and its values are provided in kwargs
    The function check if some of the parameter names corresponds to this simulation and 
    modifies the default value. Then, it launches the simulation
    '''
    print('_____________________________________________________________________________________')
    print('Starting filling simulation')

    # for item in kwargs:
    #     print(item)

    #RTM_base_name = 'Lk_RTM_40'
    RTM_lperm_file = RTM_base_name + '_modif.lperm'
    #Visual will read the variables values from a txt file that is written at the end of this section
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

    if "gaps" in kwargs:
        gaps = kwargs["gaps"]

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
    SourceVdbRTMFilePath = os.path.abspath(os.path.join(SourceDirectory, RTMVdbName))
    VdbRTMFilePath = os.path.abspath(os.path.join(outputs_files_folder, RTMVdbName))
    lpermfile = os.path.abspath(os.path.join(SourceDirectory, RTM_lperm_file))

    MacroRTMList=[]

    #Copy files to destination folder
    import shutil
    print(100 * '-')
    print('Copying to folder {}'.format(outputs_files_folder))
    print(100 * '-')
    shutil.copy(SourceVdbRTMFilePath, outputs_files_folder)

    # Internal info
    VariablesDict = {}
    VariablesDict['VdbRTMFilePath'] = VdbRTMFilePath
    VariablesDict['RTMsolverVEPath'] = RTMsolverVEPath
    VariablesDict['RTMSolverPath'] = RTMSolverPath
    VariablesDict['outputs_files_folder'] = outputs_files_folder
    VariablesDict['lpermfile'] = lpermfile

    # Default values
    VariablesDict['K11'] = 1e-9
    VariablesDict['K22'] = 1.22e-10
    VariablesDict['K33'] = 1.33e-11
    VariablesDict['Shrinkage'] = float(-.01)
    VariablesDict['Viscosity'] = 0.2
    VariablesDict['Injection_pressure'] = 500000
    VariablesDict['Injection_temperature'] = 280

    # Modified values
    if "DoE_line" in kwargs:
        print(f"DoE_line: { kwargs['DoE_line']}")
        if 'Injection_pressure' in kwargs['DoE_line']:
            MacroRTMList.append('07_RTMApplyPressure.py')
            VariablesDict['Injection_pressure'] = kwargs['DoE_line'].get('Injection_pressure')
        if 'Injection_temperature' in kwargs['DoE_line']:
            MacroRTMList.append('07_RTMApplyTemperature.py')
            VariablesDict['Injection_temperature'] = kwargs['DoE_line'].get('Injection_temperature')

    RTM_parameters_list = ['Injection_pressure', 'Injection_temperature', 'Injection flow_rate']

    MacroRTMList.append('08_RTMWriteSolverInput.py')

    # PAM-RTM uses its own python instance. A txt file is used to send it the required information
    #notes:
        #variables txt file must be in the same folder as the scripts
    f = open(os.path.join(VariablesTxtPath), "w+")
    for elem in VariablesDict:
        f.write(str(elem) + "= " + str(VariablesDict[elem]) + "\n")
    f.close()

    # %% RTM
    # Initialize application class from input data
    RTMmodel = Visual_API()
    RTMmodel.FileName = RTM_base_name
    RTMmodel.SourceFilesPath = SourceDirectory
    RTMmodel.solverPath = RTMSolverPath
    RTMmodel.solverVEPath = RTMsolverVEPath
    RTMmodel.basefolder = outputs_files_folder
    RTMmodel.RTMbasefolder = outputs_files_folder
    RTMmodel.inputFile = VdbRTMFilePath
    RTMmodel.VariablesTxtPath = VariablesTxtPath
    RTMmodel.simtype = 'RTM'
    RTMmodel.machine = machine
    OutputfileName = RTM_base_name + '.out'
    RTMmodel.outputFile = os.path.join(outputs_files_folder, OutputfileName)
    RTMmodel.display = display
    RTMmodel.fp = 1  # Floating point precision (1: SP , 2: DP , note IMPLICIT requires DP)
    RTMmodel.nt = 2  # Number of threads
    RTMmodel.mp = 1  # 1 (default): SMP parallel mode; 2: DMP parallel mode
    
  
    # Execute macros
    for elem in MacroRTMList:
        RTMmodel.LaunchMacro(elem)
    # Run    
    RTMmodel.solveStep(runInBackground=False)

    return