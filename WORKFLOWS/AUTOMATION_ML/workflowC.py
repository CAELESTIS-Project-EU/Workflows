import os
import numpy as np

from PHASES.utils import phase
from PHASES.utils import check_license

from pycompss.api.api import compss_wait_on
from pycompss.api.task import task
from pycompss.api.parameter import *
PAM_NP = 24

def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    global PAM_NP
    import time
    if "PAM_NP" in parameters:
        PAM_NP=int(parameters["PAM_NP"])
    #
    # Sampling and results folder
    #
    sample_set, DoE_names = phase.run(phases.get("Sampling"), inputs, outputs, parameters, data_folder, locals())
    sample_set = compss_wait_on(sample_set)
    DoE_names = compss_wait_on(DoE_names)
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    # Check license
    check_license_run = check_license.check_license()
    # Write input DoE file
    write_file(results_folder, sample_set, "xFile.npy")
    if check_license_run:
        y = []
        for index, row in sample_set.iterrows():
            line_number = 'line' + str(index+1)
            simulation_wdir = os.path.join(execution_folder, "SIMULATIONS") # Simulations wdir Alya
            row_folder = os.path.join(results_folder, line_number)
            if not os.path.isdir(row_folder):
                os.makedirs(row_folder)
            DoE_line = dict(zip(DoE_names, row))
            #
            # PAM-COMPOSITES simulations
            #
            sim_out = phase.run(phases.get("PAM-COMPOSITE_Simulations"), inputs, outputs, parameters, data_folder, locals())
            #
            # Postprocess PAM-COMPOSITES simulations
            #
            post_pam = phase.run(phases.get("PAM-COMPOSITE_PostProcess"), inputs, outputs, parameters, data_folder, locals(), out=sim_out)
            #
            # ALYA simulation
            #
            if "Prepare_Data" in phases:
                prepare_out = phase.run(phases.get("Prepare_Data"), inputs, outputs, parameters, data_folder, locals(), out=post_pam)
            if "ALYA_Simulation" in phases:
                alya_out = phase.run(phases.get("ALYA_Simulation"), inputs, outputs, parameters, data_folder, locals(), out=prepare_out)
            #
            # Postprocess ALYA simulation
            #
            if "ALYA_PostProcess" in phases:
                new_y = phase.run(phases.get("ALYA_PostProcess"), inputs, outputs, parameters, data_folder, locals(), out=alya_out)
                y.append(new_y)
        if "ALYA_PostProcess" in phases and "ALYA_PostProcessMerge" in phases:
            phase.run(phases.get("ALYA_PostProcessMerge"), inputs, outputs, parameters, data_folder, locals())
            write_file(results_folder, y, "yFile.npy")
    else:
        print("ERROR: PAM-COMPOSITES LICENSE IS NOT RUNNING!")
    return


@task(elements=COLLECTION_IN)
def write_file(output_folder, elements, nameFile, **kwargs):
    model_file= os.path.join(output_folder, nameFile)
    write(model_file, elements)


def write(file, element):
    with open(file, 'wb') as f3:
        np.save(f3, element)
        f3.close()
    return
