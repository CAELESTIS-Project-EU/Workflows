import os
import numpy as np
from PHASES.utils import args_values, phase
def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    #fase load for X, Y
    kernel= phase.run(phases.get("kernel_generation"), inputs, outputs, parameters, data_folder, locals())
    phase.run(phases.get("model_creation"), inputs, outputs, parameters, data_folder, locals(), out=kernel)
    return
