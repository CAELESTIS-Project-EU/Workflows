from pycompss.api.api import compss_wait_on
import numpy as np
from pycompss.api.task import task
from pycompss.api.parameter import *
from PHASES.utils import args_values, phase
import os


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    sample_set = phase.run(phases.get("sampler"), inputs, outputs, parameters, data_folder, locals())
    sample_set = compss_wait_on(sample_set)
    original_name_sim = parameters.get("original_name_sim")
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    write_file(results_folder, sample_set, "xFile.npy")
    y = []
    for i in range(sample_set.shape[0]):
        values = sample_set[i, :]
        case_name = "case_" + str(i + 1)
        simulation_wdir = execution_folder + "/SIMULATIONS/" + case_name
        name_sim = phase.run(phases.get("mesher"), inputs, outputs, parameters, data_folder, locals())
        sim_out = phase.run(phases.get("sim"), inputs, outputs, parameters, data_folder, locals(), out=name_sim)
        post_p_out = phase.run(phases.get("post_process"), inputs, outputs, parameters, data_folder, locals(),out=sim_out)
    simulation_wdir = execution_folder + "/SIMULATIONS/"
    sim_out = phase.run(phases.get("join_cases"), inputs, outputs, parameters, data_folder, locals(),out=post_p_out)
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