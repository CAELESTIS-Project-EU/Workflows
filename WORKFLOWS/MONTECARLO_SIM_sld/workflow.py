from PHASES.utils import args_values, phase
from pycompss.api.api import compss_wait_on
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
        values = sample_set[i, :]
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
    phase.run(args_values.get_values(phases.get("post_process_merge"), yaml_file, data_folder, locals()), out=y)
    return
