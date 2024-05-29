import os
from PHASES.utils import args_values, phase
from pycompss.api.api import compss_wait_on

def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    X, Y = phase.run(phases.get("load"), inputs, outputs, parameters, data_folder, locals())
    X=compss_wait_on(X)
    Y=compss_wait_on(X)

    print(f"X: {X}")
    print(f"Y: {Y}")

    kernel= phase.run(phases.get("kernel_generation"), inputs, outputs, parameters, data_folder, locals())
    kernel = compss_wait_on(kernel)
    print(f"kernel: {kernel}")
    phase.run(phases.get("model_creation"), inputs, outputs, parameters, data_folder, locals(), out=kernel)
    return
