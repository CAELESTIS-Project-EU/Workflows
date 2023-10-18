from  SALib.sample import morris as morrisSampler
import numpy as np
import sys
import importlib
import re

def problem_def(data):
    number = int(data.get("num_vars"))
    names = []
    covs = []
    means = []
    sigmas = []
    for item in data.get('variables-sampler'):
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


def get_names(problem):
    variables = problem.get("variables-sampler")
    names = []
    for item in variables:
        for key, value in item.items():
            names.append(key)
    return names


def sampling(problem, **kwargs):
    parameters= kwargs.get("parameters")
    for parameter in parameters:
        if(parameter.get("r")!=None):
            r= parameter.get("r")
        elif(parameter.get("p")!=None):
            p= parameter.get("p")
    if (r == None or p==None):
        sys.exit("r or p parameters for Morris's sempler is missing")
    else:
        N = r * (int(problem["num_vars"]) + 1)
        param_values = morrisSampler.sample(problem, N=N, optimal_trajectories=r, num_levels=p)
        return param_values

def vars_func(data, param_values, variables_fixed, names):
    calls = data.get("variables-derivate")
    variables = []
    for i in range(len(param_values)):
        value = {names[i]: param_values[i]}
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
