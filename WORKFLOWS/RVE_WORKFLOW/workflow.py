import numpy as np
from PHASES.utils import phase
from pycompss.api.api import compss_wait_on
from pycompss.api.task import task
from pycompss.api.parameter import *
import os


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    for i in range(parameters.get("n_cases")):
        simulation_wdir = execution_folder + "/SIMULATIONS/s" + str(i) + "/"
        phase.run(phases.get("rve_mesh"), inputs, outputs, parameters, data_folder, locals())
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