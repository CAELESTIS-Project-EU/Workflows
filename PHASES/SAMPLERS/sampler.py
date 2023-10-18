import importlib
from pycompss.api.task import task
from pycompss.api.parameter import *


def problem_def(type, problem, **kwargs):
    module = importlib.import_module('PHASES.SAMPLERS.' + type)
    problem_def = getattr(module, 'problem_def')(problem, **kwargs)
    return problem_def


@task(returns=1)
def sampler(type, problem, **kwargs):
    module = importlib.import_module('PHASES.SAMPLERS.' + type)
    param_values = getattr(module, 'sampling')(problem, **kwargs)
    return param_values


"""@task(returns=1)
def sampler_fie(type, problem):
    module = importlib.import_module('PHASES.SAMPLERS.' + type)
    param_values = getattr(module, 'fie_sampling')(problem)
    return param_values"""

@task(returns=1)
def vars_func(type, data, variables, variables_fixed, names):
    module = importlib.import_module('PHASES.SAMPLERS.' + type)
    variables = getattr(module, 'vars_func')(data, variables, variables_fixed, names)
    return variables


"""@task(variables_fie=COLLECTION_IN)
def vars_func(type, data, variables_fie, variables_fixed, names):
    module = importlib.import_module('PHASES.SAMPLERS.' + type)
    variables_fie = getattr(module, 'vars_func')(data, variables_fie, variables_fixed, names)
    return variables_fie"""

def get_names(type, problem):
    module = importlib.import_module('PHASES.SAMPLERS.' + type)
    variables_fie = getattr(module, 'get_names')(problem)
    return variables_fie