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
