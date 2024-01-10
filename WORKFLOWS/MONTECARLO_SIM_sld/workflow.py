from PHASES.SAMPLERS import sampler
# from PHASES.POSTSIMULATION import postSimulation
# from PHASES.BEFORESIMULATION import parserSimulation as parserSim
from PHASES.utils import args_values, phase
from pycompss.api.api import compss_wait_on
import os


def execution(yaml_file, execution_folder, data_folder, parameters):
    phases = yaml_file.get("phases")
    workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters)
    return


def workflow_execution(phases, yaml_file, execution_folder, data_folder, parameters):
    sampler_type, sampler_args = get_values(phases.get("sampler"), yaml_file, data_folder, locals())
    sample_set = sampler.sampler(sampler_type, sampler_args)
    sample_set = compss_wait_on(sample_set)
    original_name=parameters.get("name_sim")
    y = []
    for i in range(sample_set.shape[0]):
        values = sample_set[i, :]
        name_sim= original_name + "-s" + str(i)
        simulation_wdir = execution_folder + "/SIMULATIONS/" + name_sim + "/"
        results_folder = execution_folder + "/results/"
        if not os.path.isdir(results_folder):
            os.makedirs(results_folder)

        #prepare_type, prepare_args = get_values(phases.get("prepare_data"), yaml_file, data_folder, locals())
        #out1 = parserSim.prepare_data(prepare_type, prepare_args)
        prepare_out = phases.run(get_values(phases.get("prepare_data"), yaml_file, data_folder, locals()))

        #sim_type, sim_args = get_values(phases.get("sim"), yaml_file, data_folder, locals())
        #out = sim.run_sim(sim_type, sim_args, out=out1)
        sim_out = phases.run(get_values(phases.get("sim"), yaml_file, data_folder, locals()),out=prepare_out)
        #post_process_type, post_process_args = get_values(phases.get("post_process"), yaml_file, data_folder, locals())
        new_y = phases.run(get_values(phases.get("post_process"), yaml_file, data_folder, locals()), out=sim_out)
        #new_y = postSimulation.collect(post_process_type, post_process_args, out=out)
        y.append(new_y)
    #write_file_type, write_file_args = get_values(phases.get("post_process_merge"), yaml_file, data_folder, locals())
    phases.run(get_values(phases.get("post_process_merge"), yaml_file, data_folder, locals()))
    #postSimulation.write_file(write_file_type, write_file_args)
    return
def get_values(phase, yaml_file, data_folder, symbol_table):
    phase_type = phase.get("type")
    args_dict = None
    if phase.get("arguments"):
        args = phase.get("arguments")
        if args:
            args_dict = get_arguments(args, yaml_file, data_folder, symbol_table)
            return phase_type, args_dict


def get_arguments(phase_args, yaml_file, data_folder, symbol_table):
    args = []
    for phase_arg in phase_args:
        for key, value in phase_arg.items():
            if starts_with_dollar(str(value)):
                search_params = remove_dollar_prefix(value)
                first_part, second_part = extract_parts(search_params)
                args.append(switch_values(first_part, second_part, yaml_file, data_folder, symbol_table))
            else:
                args[key] = value
    return args


def switch_values(first_part, second_part, yaml_file, data_folder, symbol_table):
    if first_part == "outputs":
        return args_values.get_outputs(second_part, yaml_file.get("outputs"))
    elif first_part == "inputs":
        return args_values.get_inputs(second_part, yaml_file.get("inputs"), data_folder)
    elif first_part == "parameters":
        return args_values.get_param(second_part, yaml_file.get("parameters"))
    elif first_part == "variables":
        return add_entry(second_part, get_variable_value(second_part, symbol_table))
    else:
        raise ValueError(f"Unsupported first_part value: {first_part}")


def extract_parts(input_string):
    parts = input_string[1:].split('.')
    if len(parts) >= 2:
        first_part = parts[0]
        second_part = ".".join(parts[1:])
        return first_part, second_part
    else:
        return None, None


def remove_dollar_prefix(s):
    return s[1:] if s.startswith("$") else s


def starts_with_dollar(input_string):
    return input_string.startswith("$")


def add_entry(key, value):
    new_entry = {key: value}
    return new_entry


def get_variable_value(variable_name, symbol_table):
    if variable_name in symbol_table:
        return symbol_table[variable_name]
    else:
        return f"Variable '{variable_name}' not found."
