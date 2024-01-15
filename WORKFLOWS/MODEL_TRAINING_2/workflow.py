import os
import numpy as np
from PHASES.utils import args_values, phase
def execution(yaml_file, execution_folder, data_folder, parameters):
    phases = yaml_file.get("phases")
    workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters)
    return

def workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters):
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    kernel= phase.run(args_values.get_values(phases.get("kernel_generation"), yaml_file, data_folder, locals()))
    phase.run(args_values.get_values(phases.get("training"), yaml_file, data_folder, locals()), out=kernel)
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


