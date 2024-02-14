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
        print("RUN SIM")
        print(phases.get("sim"))
        sim_out = phase.run(args_values.get_values(phases.get("sim"), yaml_file, data_folder, locals()),
                            out=prepare_out)
        print("POST_PROCESS COLLECT")
        print(phases.get("post_process"))
        new_y = phase.run(args_values.get_values(phases.get("post_process"), yaml_file, data_folder, locals()),
                          out=sim_out)
        print("NEW Y")
        print(new_y)
        y.append(new_y)
        print(y)
    out_post=phase.run(args_values.get_values(phases.get("post_process_merge"), yaml_file, data_folder, locals()))
    phase.run(args_values.get_values(phases.get("sensitivity"), yaml_file, data_folder, locals()), out=out_post)
    return
