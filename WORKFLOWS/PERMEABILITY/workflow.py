#from pycompss.api.api import compss_wait_on
from PHASES.utils import args_values, phase
import os


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    sample_set = phase.run(
        args_values.get_values(phases.get("sampler"), inputs, outputs, parameters, data_folder, locals()))
    sample_set = compss_wait_on(sample_set)
    original_name_sim = parameters.get("original_name_sim")
    y = []
    for i in range(sample_set.shape[0]):
        values = sample_set[i, :]
        case_name = "case_" + str(i + 1)
        simulation_wdir = execution_folder + "/SIMULATIONS/" + case_name
        results_folder = execution_folder + "/results/"
        if not os.path.isdir(results_folder):
            os.makedirs(results_folder)
        name_sim = phase.run(
            args_values.get_values(phases.get("mesher"), inputs, outputs, parameters, data_folder, locals()))
        sim_out = phase.run(
            args_values.get_values(phases.get("sim"), inputs, outputs, parameters, data_folder, locals()), out=name_sim)
        post_p_out = phase.run(
            args_values.get_values(phases.get("post_process"), inputs, outputs, parameters, data_folder, locals()),
            out=sim_out)
    simulation_wdir = execution_folder + "/SIMULATIONS/"
    sim_out = phase.run(
        args_values.get_values(phases.get("join_cases"), inputs, outputs, parameters, data_folder, locals()),
        out=post_p_out)
    return
