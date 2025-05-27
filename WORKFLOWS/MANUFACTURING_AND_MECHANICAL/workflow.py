import os
import numpy as np
from PHASES.utils import phase
from pycompss.api.api import compss_wait_on
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.api import compss_wait_on
from PHASES.AUTOMATION_ML import check_license
PAM_NP = 1


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    global PAM_NP
    import time
    if "PAM_NP" in parameters:
        PAM_NP=int(parameters["PAM_NP"])
        print("Setting PAM NP to " + str(PAM_NP))
    df, DoE_names = phase.run(phases.get("Sampling"), inputs, outputs, parameters, data_folder, locals())
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    check_license_run=check_license.check_license()
    check_license_run = compss_wait_on(check_license_run) 
    df = compss_wait_on(df)
    DoE_names = compss_wait_on(DoE_names)
    if check_license_run:
        print("CHECK LICENSE DONE")
        a = 0
        y = []
        for index, row in df.iterrows():
            a += 1
            line_number = 'line' + str(a)
            
            os.makedirs(os.path.join(results_folder, line_number), exist_ok=True)
            DoE_line = dict(zip(DoE_names, row))
            print("DoE_line: ", DoE_line)

            sim_out = phase.run(phases.get("PAM-COMPOSITE_Simulations"), inputs, outputs, parameters, data_folder, locals())
            
            if "PAM-COMPOSITE_PostProcess" in phases:
                phase.run(phases.get("PAM-COMPOSITE_PostProcess"), inputs, outputs, parameters, data_folder, locals(), out=sim_out)

            prepare_out = phase.run(phases.get("Prepare Data"), inputs, outputs, parameters, data_folder, locals(), index=index, out=sim_out)

            alya_out = phase.run(phases.get("ALYA_Simulation"), inputs, outputs, parameters, data_folder, locals(), out=prepare_out)
            
            if "ALYA_PostProcess" in phases:
                new_y = phase.run(phases.get("ALYA_PostProcess"), inputs, outputs, parameters, data_folder, locals(), out=alya_out)
                y.append(new_y) 

        write_file(results_folder, y, "yFile.npy")
    else:
        print("LICENSE IS NOT RUNNING!")
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