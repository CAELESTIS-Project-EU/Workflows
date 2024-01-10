import importlib
from pycompss.api.task import task
from pycompss.api.parameter import *

def prepare_data(prepare_type, prepare_args):
    module_call, function_call = split_string_at_last_dot(prepare_type)
    module = importlib.import_module(module_call)
    return getattr(module, function_call)(prepare_args)

def split_string_at_last_dot(input_string):
    last_dot_index = input_string.rfind('.')

    if last_dot_index != -1:
        first_part = input_string[:last_dot_index]
        last_part = input_string[last_dot_index + 1:]
        return first_part, last_part
    else:
        # If there is no dot in the input string
        return None, None

"""@task(returns=1)
def prepare_fie_file(prepare_type, template, sim_dir, nameSim, variables, wdir, original_name, out):
    module_call, function_call = split_string_at_last_dot(prepare_type)
    module = importlib.import_module(module_call)
    return getattr(module, function_call)(variables, template, sim_dir, nameSim, wdir, original_name)

@task(returns=1)
def prepare_dom_file(prepare_type, template, data_folder, nameSim, mesh_source, out):
    module_call, function_call = split_string_at_last_dot(prepare_type)
    module = importlib.import_module(module_call)
    return getattr(module, function_call)(data_folder, nameSim, template, mesh_source)"""
