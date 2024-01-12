from PHASES.SAMPLERS import sampler
from PHASES.utils import args_values, phase
from pycompss.api.api import compss_wait_on
import os


def execution(yaml_file, execution_folder, data_folder, parameters):
    phases = yaml_file.get("phases")
    workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters)
    return


def workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters):
    # sampler_type, sampler_args = **args_values.get_values(phases.get("sampler"), yaml_file, data_folder, locals())
    sample_set = phase.run(args_values.get_values(phases.get("sampler"), yaml_file, data_folder, locals()))
    # sample_set = sampler.sampler(sampler_type, sampler_args)
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

        # prepare_type, prepare_args = get_values(phases.get("prepare_data"), yaml_file, data_folder, locals())
        # out1 = parserSim.prepare_data(prepare_type, prepare_args)
        prepare_out = phase.run(args_values.get_values(phases.get("prepare_data"), yaml_file, data_folder, locals()))

        # sim_type, sim_args = get_values(phases.get("sim"), yaml_file, data_folder, locals())
        # out = sim.run_sim(sim_type, sim_args, out=out1)
        sim_out = phase.run(args_values.get_values(phases.get("sim"), yaml_file, data_folder, locals()),
                            out=prepare_out)
        # post_process_type, post_process_args = get_values(phases.get("post_process"), yaml_file, data_folder,
        # locals())
        new_y = phase.run(args_values.get_values(phases.get("post_process"), yaml_file, data_folder, locals()),
                          out=sim_out)
        # new_y = postSimulation.collect(post_process_type, post_process_args, out=out)
        y.append(new_y)
    # write_file_type, write_file_args = get_values(phases.get("post_process_merge"), yaml_file, data_folder, locals())
    phase.run(args_values.get_values(phases.get("post_process_merge"), yaml_file, data_folder, locals()), out=y)
    # postSimulation.write_file(write_file_type, write_file_args)
    return
