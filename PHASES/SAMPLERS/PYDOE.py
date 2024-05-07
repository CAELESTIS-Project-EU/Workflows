from pyDOE import *
from scipy.stats.distributions import norm, uniform, weibull_min, lognorm
import numpy as np
import importlib
import re
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(returns=1)
def sampling(problem, **kwargs):
    """sampler_args=kwargs.get("args")
    problem= get_value(sampler_args, "problem")"""
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

@task(returns=1)
def sampling_distribution(problem, **kwargs):
    """sampler_args=kwargs.get("args")
    problem= get_value(sampler_args, "problem")"""
    
    variables = problem.get("variables-sampler")
    n_samples = int(problem.get("n_samples"))
    num_var = int(problem.get("num_var"))
    
    covs = []
    means = []
    sigmas = []
    alphas = []
    betas = [] 
    typeDistr = []
    for item in variables:
        for key, value in item.items():
            distr = value.get('distr')
            mean = float(value.get("mean"))
            sigma = float(value.get('sigma'))
            cov = float(value.get('cov'))
            alpha = float(value.get('alpha'))
            beta = float(value.get('beta'))
            typeDistr.append(distr)
            means.append(mean)
            covs.append(cov)
            sigmas.append(sigma)
            alphas.append(alpha)
            betas.append(beta)
            
    lhs_sample = lhs(num_var, n_samples, criterion="maximin")
    
    samples_final = np.zeros((n_samples, num_var))
    
    for i in range(num_var):
        if typeDistr[i] == 'norm':
            samples_final[:, i] = norm(loc=means[i], scale=sigmas[i]).ppf(lhs_sample[:, i])
        elif typeDistr[i] == 'uniform':
            lower_bound = means[i] - means[i]*covs[i]/100.
            upper_bound = means[i] + means[i]*covs[i]/100.
            samples_final[:, i] = uniform(loc=lower_bound, scale=(upper_bound - lower_bound)).ppf(lhs_sample[:, i])
        elif typeDistr[i] == 'weibull': 
            samples_final[:, i] = weibull_min(betas[i], scale=alphas[i], loc=0).ppf(lhs_sample[:, i])
        elif typeDistr[i] == 'lognorm':
            samples_final[:, i] = lognorm(s=sigmas[i], loc=means[i]).ppf(lhs_sample[:, i])
            
    return samples_final

def get_value(element, param):
    if param in element:
        return element[param]
    else:
        raise ValueError(f"The key '{param}' was not found in the dictionary.")

def get_names(sampler_args):
    problem = sampler_args.get("problem")
    variables = problem.get("variables-sampler")
    names = []
    for item in variables:
        for key, value in item.items():
            names.append(key)
    return names

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
