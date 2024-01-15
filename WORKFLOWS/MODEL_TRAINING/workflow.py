import numpy as np
from PHASES.utils import args_values, phase
from pycompss.api.api import compss_wait_on
import os
import yaml


def execution(yaml_file, execution_folder, data_folder, parameters):
    phases = yaml_file.get("phases")
    workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters)
    return

def workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters):
    x = phase.run(args_values.get_values(phases.get("sampler"), yaml_file, data_folder, locals()))
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
        prepare_out = phase.run(args_values.get_values(phases.get("prepare_data"), yaml_file, data_folder, locals()))
        sim_out = phase.run(args_values.get_values(phases.get("sim"), yaml_file, data_folder, locals()),
                            out=prepare_out)
        new_y = phase.run(args_values.get_values(phases.get("post_process"), yaml_file, data_folder, locals()),
                          out=sim_out)
        y.append(new_y)
    print("PARAMS POST")
    print(args_values.get_values(phases.get("post_process_merge"), yaml_file, data_folder, locals()))
    phase.run(args_values.get_values(phases.get("post_process_merge"), yaml_file, data_folder, locals()), out=y)
    kernel= phase.run(args_values.get_values(phases.get("kernel_generation"), yaml_file, data_folder, locals()), out=y)
    phase.run(args_values.get_values(phases.get("training"), yaml_file, data_folder, locals()), out=y)

    return







def write_file_x(output_folder, x, **kwargs):
    # You can now use file_path for further processing
    model_file = output_folder + "/xFile.npy"
    write(model_file, x)


def write_file_y(output_folder, y, **kwargs):
    # You can now use file_path for further processing
    model_file = output_folder + "/yFile.npy"
    write(model_file, y)


def write(file, element):
    with open(file, 'wb') as f3:
        np.save(f3, element)
        f3.close()
    return
