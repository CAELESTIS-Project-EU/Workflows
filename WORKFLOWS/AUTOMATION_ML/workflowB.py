import os
import numpy as np

from PHASES.utils import phase

from pycompss.api.api import compss_wait_on
from pycompss.api.task import task
from pycompss.api.parameter import *

def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    #
    # Sampling and results folder
    #
    df, DoE_names = phase.run(phases.get("Sampling"), inputs, outputs, parameters, data_folder, locals())
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    df = compss_wait_on(df)
    DoE_names = compss_wait_on(DoE_names)
    a = 0
    y = []
    for index, row in df.iterrows():
        a += 1
        line_number = 'line' + str(a)
        simulation_wdir = os.path.join(execution_folder, "SIMULATIONS") # Simulations wdir Alya
        row_folder = os.path.join(results_folder, line_number)
        if not os.path.isdir(row_folder):
           os.makedirs(row_folder)
        DoE_line = dict(zip(DoE_names, row))
        #
        # ALYA simulation
        #
        prepare_out = phase.run(phases.get("Prepare Data"), inputs, outputs, parameters, data_folder, locals(), index=index)#, out=sim_out)
        alya_out = phase.run(phases.get("ALYA_Simulation"), inputs, outputs, parameters, data_folder, locals(), out=prepare_out)
        #
        # Postprocess ALYA simulation
        #
        new_y = phase.run(phases.get("ALYA_PostProcess"), inputs, outputs, parameters, data_folder, locals(), out=alya_out)
        y.append(new_y)
    phase.run(phases.get("ALYA_PostProcessMerge"), inputs, outputs, parameters, data_folder, locals())
    write_file(results_folder, y, "yFile.npy")
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
