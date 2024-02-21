import numpy as np
from PHASES.utils import args_values, phase
from pycompss.api.api import compss_wait_on
import os
import yaml


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    x = phase.run(args_values.get_values(phases.get("sampler"), inputs, outputs, parameters, data_folder, locals()))
    x = compss_wait_on(x)
    original_name_sim = parameters.get("original_name_sim")
    y = []
    for i in range(x.shape[0]):
        values = x[i, :]
        name_sim = original_name_sim + "-s" + str(i)
        simulation_wdir = execution_folder + "/SIMULATIONS/" + name_sim + "/"
        results_folder = execution_folder + "/results/"
        if not os.path.isdir(results_folder):
            os.makedirs(results_folder)
        prepare_out = phase.run(args_values.get_values(phases.get("prepare_data"), inputs, outputs, parameters, data_folder, locals()))
        sim_out = phase.run(args_values.get_values(phases.get("sim"), inputs, outputs, parameters, data_folder, locals()),
                            out=prepare_out)
        new_y = phase.run(args_values.get_values(phases.get("post_process"), inputs, outputs, parameters, data_folder, locals()),
                          out=sim_out)
        y.append(new_y)
    phase.run(args_values.get_values(phases.get("post_process_merge"), inputs, outputs, parameters, data_folder, locals()), out=y)
    kernel= phase.run(args_values.get_values(phases.get("kernel_generation"), inputs, outputs, parameters, data_folder, locals()), out=y)
    phase.run(args_values.get_values(phases.get("training"), inputs, outputs, parameters, data_folder, locals()), out=y)
    write_file(results_folder, x, "xFile.npy")
    write_file(results_folder, y, "yFile.npy")
    return

def write_file(output_folder, elements, nameFile, **kwargs):
    model_file= os.path.join(output_folder, nameFile)
    write(model_file, elements)



def write(file, element):
    with open(file, 'wb') as f3:
        np.save(f3, element)
        f3.close()
    return
