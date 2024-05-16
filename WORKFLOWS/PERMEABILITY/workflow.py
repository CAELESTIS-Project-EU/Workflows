from pycompss.api.api import compss_wait_on, compss_barrier

import numpy as np
from pycompss.api.task import task
from pycompss.api.parameter import *
from PHASES.utils import args_values, phase
import os



def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    data_set = phase.run(phases.get("sampler"), inputs, outputs, parameters, data_folder, locals())
    data_set = compss_wait_on(data_set)
    original_name_sim = parameters.get("original_name_sim")
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    write_file(results_folder, data_set, "xFile.npy")
    y = []
    for i, values in data_set.iterrows():
        case_name = "case_" + str(i)
        print(f"values {values}")
        simulation_wdir = execution_folder + "/SIMULATIONS/" + case_name
        name_sim = phase.run(phases.get("mesher"), inputs, outputs, parameters, data_folder, locals())
        sim_out = phase.run(phases.get("sim"), inputs, outputs, parameters, data_folder, locals(), out=name_sim)
        new_result = phase.run(phases.get("post_process"), inputs, outputs, parameters, data_folder, locals(),out=sim_out)
        y.append(new_result)
    simulation_wdir = execution_folder + "/SIMULATIONS/"
    sim_out = phase.run(phases.get("join_cases"), inputs, outputs, parameters, data_folder, locals(), out=y)
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