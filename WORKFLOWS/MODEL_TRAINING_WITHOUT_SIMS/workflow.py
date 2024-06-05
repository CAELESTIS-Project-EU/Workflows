import os
from PHASES.utils import args_values, phase

def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    X, Y = phase.run(phases.get("load"), inputs, outputs, parameters, data_folder, locals())
    print(f"X shape: {X.shape}")
    print(f"X _n_blocks: {X._n_blocks}")
    print(f"X len blocks: {len(X._blocks)}")
    print(f"X len block 0: {len(X._blocks[0])}")
    #kernel= phase.run(phases.get("kernel_generation"), inputs, outputs, parameters, data_folder, locals())
    #phase.run(phases.get("model_creation"), inputs, outputs, parameters, data_folder, locals(), out=kernel)
    return
