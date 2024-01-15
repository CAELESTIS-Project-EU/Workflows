from  SALib.sample import morris as morrisSampler
import numpy as np
import sys
import importlib
import re
from pycompss.api.task import task
from pycompss.api.parameter import *
@task(returns=1)
def problem_def(problem,**kwargs):
    number = int(problem.get("num_vars"))
    names = []
    covs = []
    means = []
    sigmas = []
    for item in problem.get('variables-sampler'):
        for key, value in item.items():
            names.append(key)
            means.append(value['mean'])
            covs.append(value['cov'])
    for i in range(0, len(means)):
        sigma = (float(means[i]) * float(covs[i])) / 100
        sigmas.append(sigma)
    bounds = np.zeros((len(means), 2))
    for i in range(0, len(means)):
        bounds[i, 0] = float(means[i]) - (3 * float(sigmas[i]))
        bounds[i, 1] = float(means[i]) + (3 * float(sigmas[i]))
    problem = {
        'num_vars': number,
        'names': names,
        'bounds': bounds
    }
    return problem

def get_names(sampler_args):
    problem = sampler_args.get("problem")
    variables = problem.get("variables-sampler")
    names = []
    for item in variables:
        for key, value in item.items():
            names.append(key)
    return names

@task(returns=1)
def sampling(problem, **kwargs):
    probDef= problem_def(problem, p, r, **kwargs)
    if (r == None or p==None):
        sys.exit("r or p parameters for Morris's sempler is missing")
    else:
        N = r * (int(probDef["num_vars"]) + 1)
        param_values = morrisSampler.sample(probDef, N=N, optimal_trajectories=r, num_levels=p)
        return param_values

@task(returns=1)
def vars_func(sampler_args, variables_sampled):
    names=get_names(sampler_args)
    problem = sampler_args.get("problem")
    variables_fixed= problem.get("variables-fixed")
    calls = problem.get("variables-derivate")
    variables = []
    for i in range(len(variables_sampled)):
        value = {names[i]: variables_sampled[i]}
        variables.append(value)
    for variable_fixed in variables_fixed:
        variables.append(variable_fixed)
    for name, value in calls.items():
        call = value
        head, tail = call.get("method").split(".")
        parameters = call.get("parameters")
        args = []
        for parameter in parameters:
            if re.search("eval\(", parameter):
                s = parameter.replace('eval(', '')
                s = s.replace(')', '')
                res = callEval(s, variables)
                args.append(res)
            else:
                args.append(loop(parameter, variables))
        module = importlib.import_module('PHASES.TRANSFORMATIONS.' + head)
        c = getattr(module, tail)(*args)
        outputs = call.get("outputs")
        for i in range(len(outputs)):
            var = {outputs[i]: c[i]}
            variables.append(var)
    return variables

def callEval(parameter, variables):
    groups = re.split(r'\b', parameter)
    for group in groups:
        if group != "":
            if not group.isnumeric():
                for variable in variables:
                    if group in variable:
                        var = variable.get(group)
                        parameter= parameter.replace(group, str(var))
                        break
    res = eval(parameter)
    return res


def loop(parameter, variables):
    for variable in variables:
        if parameter in variable:
            var = variable.get(parameter)
            return var


def get_value(element, param):
    if param in element:
        return element[param]
    else:
        raise ValueError(f"The key '{param}' was not found in the dictionary.")