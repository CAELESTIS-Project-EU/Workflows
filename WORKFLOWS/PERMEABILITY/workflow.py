from pycompss.api.api import compss_wait_on
from PHASES.utils import args_values, phase
import os


def execution(yaml_file, execution_folder, data_folder, parameters):
    phases = yaml_file.get("phases")
    workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters)
    return


def workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters):
    sample_set = phase.run(args_values.get_values(phases.get("sampler"), yaml_file, data_folder, locals()))
    sample_set = compss_wait_on(sample_set)
    original_name_sim = parameters.get("original_name_sim")
    y = []
    for i in range(sample_set.shape[0]):
        angles_tows = [sample_set[i, 0], sample_set[i, 1], sample_set[i, 2], sample_set[i, 3]]
        L_pro = sample_set[i, 4]
        name_sim = original_name_sim + "-s" + str(i)
        simulation_wdir = execution_folder + "/SIMULATIONS/"
        results_folder = execution_folder + "/results/"
        if not os.path.isdir(results_folder):
            os.makedirs(results_folder)
        name_sim = phase.run(args_values.get_values(phases.get("mesher"), yaml_file, data_folder, locals()))
        path=execution_folder + "/SIMULATIONS/"+ name_sim
        sim_out = phase.run(args_values.get_values(phases.get("sim"), yaml_file, data_folder, locals()))
    return
