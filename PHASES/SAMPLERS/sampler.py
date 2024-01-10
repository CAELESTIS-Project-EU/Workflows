import importlib
from pycompss.api.task import task
from pycompss.api.parameter import *


def problem_def(type, problem, **kwargs):
    module_call, function_call = split_string_at_last_dot(type)
    module = importlib.import_module(module_call)
    problem_def = getattr(module, function_call)(problem, **kwargs)
    return problem_def


@task(returns=1)
def sampler(type, sampler_args, **kwargs):
    module_call, function_call = split_string_at_last_dot(type)
    module = importlib.import_module(module_call)
    param_values = getattr(module, function_call)(**sampler_args, **kwargs)
    return param_values

@task(returns=1)
def vars_func(type, sampler_args, variables):
    module_call, function_call = split_string_at_last_dot(type)
    module = importlib.import_module(module_call)
    variables = getattr(module, function_call)(sampler_args, variables)
    return variables

"""def get_names(type, sampler_args):
    module = importlib.import_module('PHASES.SAMPLERS.' + type)
    variables_fie = getattr(module, 'get_names')(sampler_args)
    return variables_fie"""


def split_string_at_last_dot(input_string):
    last_dot_index = input_string.rfind('.')

    if last_dot_index != -1:
        first_part = input_string[:last_dot_index]
        last_part = input_string[last_dot_index + 1:]
        return first_part, last_part
    else:
        # If there is no dot in the input string
        return None, None