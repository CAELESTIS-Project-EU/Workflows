from pyDOE import *
from scipy.stats.distributions import norm
import numpy as np
import importlib
import re
from pycompss.api.task import task
from pycompss.api.parameter import *
@task(returns=1)
def sampling(sampler_args, **kwargs):
    print("sampler_args ", sampler_args)
    problem= get_value(sampler_args, "problem")
    print("problem ", problem)
    variables = problem.get("variables-sampler")
    ratio = problem.get("ratio_norm")
    n_samples = int(problem.get("n_samples"))
    criterion_type = problem.get("criterion")
    num_var = int(problem.get("num_var"))
    covs = []
    means = []
    sigmas = []
    for item in variables:
        for key, value in item.items():
            mean = float(value.get("mean"))
            sigma = value.get('sigma', None)
            cov = value.get('cov', None)
            means.append(mean)
            if sigma:
                sigmas.append(float(sigma))
            elif cov:
                cov= float(cov)
                covs.append(cov)
                sigma=(mean * cov)/100
                sigmas.append(sigma)
    samples_norm = int(ratio * n_samples)
    samples_uni = n_samples - int(samples_norm)
    bounds = np.zeros((len(means), 2))
    for i in range(0, len(means)):
        bounds[i, 0] = means[i] - (3 * sigmas[i])
        bounds[i, 1] = means[i] + (3 * sigmas[i])
    lhs_sample = lhs(num_var, n_samples, criterion=criterion_type)
    design_norm = np.zeros((n_samples, num_var))
    design_uni = np.zeros((n_samples, num_var))
    for i in range(num_var):
        design_norm[:, i] = norm(loc=means[i], scale=sigmas[i]).ppf(lhs_sample[:, i])
        design_uni[:, i] = bounds[i, 0] + ((bounds[i, 1] - bounds[i, 0]) * lhs_sample[:, i])
    sample_uni_extract = design_uni[0:samples_uni, :]
    sample_norm_extract = design_norm[0:samples_norm, :]
    samples_final = np.concatenate((sample_uni_extract, sample_norm_extract))
    return samples_final



def get_value(element, param):
    for item in element:
        if param in item:
            problem_dict = item['problem']
            return problem_dict
    else:
        raise ValueError

def get_names(sampler_args):
    problem = sampler_args.get("problem")
    variables = problem.get("variables-sampler")
    names = []
    for item in variables:
        for key, value in item.items():
            names.append(key)
    return names

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