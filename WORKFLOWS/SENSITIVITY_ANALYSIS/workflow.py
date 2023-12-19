from PHASES.SENSITIVITY import sensitivity as sens
from PHASES.SIMULATIONS import simulation as sim
from PHASES.BEFORESIMULATION import parserSimulation as parserSim
from PHASES.POSTSIMULATION import postSimulation as postSimulation
from PHASES.SAMPLERS import sampler
from pycompss.api.api import compss_wait_on
import os
import yaml


def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases = data.get("phases")
        workflow_execution(phases, data.get("parameters"), data.get("inputs"), data.get("outputs"), execution_folder,data_folder)

        workflow_execution(phases.get("sampler"), phases.get("sim"), phases.get("sens"), data.get("problem"),
                           execution_folder, data.get("outputs"), data.get("input"), data_folder)
    return


def workflow_execution(phases, parameters_yaml, inputs_yaml, outputs_yaml, execution_folder, data_folder):
    sampler_type, sampler_param=get_values(phases.get("sampler"), inputs_yaml, outputs_yaml, parameters_yaml, data_folder)
    sim_type, sim_input, sim_outputs, sim_params= get_values(phases.get("sim"), inputs_yaml, outputs_yaml, parameters_yaml, data_folder)
    sens_type, sens_outputs, sens_params= get_values(phases.get("sens"), inputs_yaml, outputs_yaml, parameters_yaml, data_folder)

    problem = sampler_param.get("problem")
    mesh = sim_input.get("mesh")
    templateSld = sim_input.get("template_sld")
    templateDom = sim_input.get("template_dom")
    
    problemDef = sampler.problem_def(sampler_type, problem)
    param_values = sampler.sampler(sampler_type, problemDef, parameters=sampler_param)
    param_values = compss_wait_on(param_values)
    names = sampler.get_names(sampler_type, problem)
    parent_directory, original_name = os.path.split(mesh)
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    y = []
    for i in range(len(param_values)):
        simulation_wdir = execution_folder + "/SIMULATIONS/" + original_name + "-s" + str(i) + "/"
        if not os.path.isdir(simulation_wdir):
            os.makedirs(simulation_wdir)
        nameSim = original_name + "-s" + str(i)
        values = param_values[i, :]
        variables = sampler.vars_func(sampler_type, problem, values, problem.get("variables-fixed"), names)
        out1 = parserSim.prepare_data(sim_type, mesh, templateSld, simulation_wdir, original_name, nameSim,
                                      variables)
        out3 = parserSim.prepare_dom_file(sim_type, templateDom, simulation_wdir, nameSim, mesh, out1)
        out = sim.run_sim(sim_type, simulation_wdir, nameSim, out3=out3)
        new_y = postSimulation.collect(sim_type, simulation_wdir, nameSim, out)
        y.append(new_y)
    postSimulation.write_file(sim_type, results_folder, y, outputs=sim_outputs)
    out5 = sens.analysis(problemDef, y, results_folder, param_values, parameters=sens_type, paramSampling=phases.get("sampler"),
                         outputs=sens_outputs)
    # new code
    # res= sens.generate_path(sampler_type, results_folder, outputs, out5)
    return


def get_values(phase, inputs_yaml, outputs_yaml, parameters_yaml, data_folder):
    phase_type= phase.get("type")
    print("PHASE:", str(phase_type))
    outputs_dict=None
    inputs_dict=None
    parameters_dict=None
    if phase.get("outputs"):
        outputs=phase.get("outputs")
        if outputs:
            outputs_dict= get_outputs(outputs, outputs_yaml, data_folder)
    if phase.get("inputs"):
        inputs=phase.get("inputs", [])
        if inputs:
            inputs_dict= get_inputs(inputs, inputs_yaml, data_folder)
    if phase.get("parameters"):
        parameters=phase.get("parameters")
        if parameters:
            parameters_dict= get_param(parameters, parameters_yaml)
    return tuple(value for value in [phase_type, inputs_dict, outputs_dict, parameters_dict] if value is not None)


def get_param(phase_parameters, parameters_yaml):
    parameters={}
    for param_item in phase_parameters:
        # Iterate through each key-value pair in the input item
        for key, value in param_item.items():
            if starts_with_dollar(str(value)):
                search_params= remove_dollar_prefix(value)
                param= extract_value(parameters_yaml, search_params)
                parameters[key]=param
            else:
                parameters[key]=value
    print("parameters: ", str(parameters))
    return parameters

def get_inputs(phase_input, input_yaml, data_folder):
    inputs={}
    for input_item in phase_input:
        # Iterate through each key-value pair in the input item
        for key, value in input_item.items():
            search_input= remove_dollar_prefix(value)
            input_folder= extract_value_files(input_yaml, search_input)
            input_folder = os.path.join(data_folder, input_folder) if input_folder else None
            inputs[key]=input_folder
    print("inputs: ", str(inputs))
    return inputs

def get_outputs(phase_outputs, outputs_yaml, data_folder):
    outputs={}
    for outputs_item in phase_outputs:
        for key, value in outputs_item.items():
            search_outputs= remove_dollar_prefix(value)
            outputs_folder= extract_value_files(outputs_yaml, search_outputs)
            outputs_folder = os.path.join(data_folder, outputs_folder) if outputs_folder else None
            outputs[key]=outputs_folder
    print("outputs: ", str(outputs))
    return outputs

def extract_value(yaml, name):
    value = yaml.get(name, [])
    return value

def extract_value_files(yaml, name):
    value = yaml.get(name, [])
    value_folder = ""
    for item in value:
        if isinstance(item, dict) and 'path' in item:
            value_folder = item['path']
            break
    return value_folder
def remove_dollar_prefix(s):
    """
    Removes the dollar sign from the beginning of a string, if it exists.

    :param s: The string to process
    :return: The string with the dollar sign removed, if it was present
    """
    return s[1:] if s.startswith("$") else s

def starts_with_dollar(input_string):
    """
    Check if the input string starts with '$'.

    :param input_string: The string to check
    :return: True if the string starts with '$', False otherwise
    """
    return input_string.startswith("$")