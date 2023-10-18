from  SALib.sample import saltelli as saltelliSampler
import sys
import importlib
import re

def sampling(self, problem, **kwargs):
    parameters = kwargs.get("parameters")
    for parameter in parameters:
        if (parameter.get("N") != None):
            N = parameter.get("N")
    if (N == None):
        sys.exit("r or p parameters for Saltelli's sampler is missing")
    else:
        param_values = saltelliSampler.sample(problem, N)
        return param_values

def vars_func(data, param_values, variables_fixed):
    calls = data.get("variables-derivate")
    variables = []
    names = data.get("variables-sampler")
    for i in range(len(param_values)):
        value = {(list(names[i])[0]): param_values[i]}
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
                        print("GROUP")
                        print(group)
                        print("VAR")
                        print(var)
                        parameter= parameter.replace(group, str(var))
                        print(parameter)
                        break
    res = eval(parameter)
    print("EVAL")
    print(res)
    return res


def loop(parameter, variables):
    for variable in variables:
        if parameter in variable:
            var = variable.get(parameter)
            return var
