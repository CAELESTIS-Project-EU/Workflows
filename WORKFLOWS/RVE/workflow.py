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
    simulation_folder = execution_folder + "/SIMULATIONS/"
    if not os.path.isdir(simulation_folder):
        os.makedirs(simulation_folder)
    for i in range(parameters.get("n_cases")):
        simulation_wdir = simulation_folder + "/SIMULATION-s" + str(i) + "/"
        #out_gen_data= phase.run(phases.get("rve_gen"), inputs, outputs, parameters, data_folder, locals())
        out_msh= phase.run(phases.get("rve_mesher"), inputs, outputs, parameters, data_folder, locals())
        out_solver=phase.run(phases.get("rve_solver"), inputs, outputs, parameters, data_folder, locals(), out=out_msh)
        sim_out = phase.run(phases.get("sim"), inputs, outputs, parameters, data_folder, locals(), out=out_solver)
    #collect_alya_result
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