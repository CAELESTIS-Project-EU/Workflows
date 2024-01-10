import importlib
import os
import re
import shutil
from pycompss.api.task import task
from pycompss.api.parameter import *


def prepare_data(prepare_args):
    variables = vars_func(prepare_args)
    out1 = prepare_sld(prepare_args, variables)
    if prepare_args.get("template_fie"):
        out2 = prepare_fie(prepare_args, variables, out=out1)
    if prepare_args.get("template_dom"):
        out3 = prepare_dom(prepare_args, variables, out=out1)
    return


@task(returns=1)
def vars_func(prepare_args, **kwargs):
    variables_sampled = prepare_args.get("values")
    names = get_names(prepare_args)
    problem = prepare_args.get("problem")
    variables_fixed = problem.get("variables-fixed")
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


@task(returns=1)
def prepare_sld(prepare_args, variables, **kwargs):
    original_name = prepare_args.get("name_sim")
    template = prepare_args.get("template_sld")
    mesh = prepare_args.get("mesh")
    simulation_wdir = prepare_args.get("simulation_wdir")
    nameSim = prepare_args.get("nameSim")
    # simulation_wdir = execution_folder + "/SIMULATIONS/" + original_name + "-s" + str(i) + "/"
    if not os.path.isdir(simulation_wdir):
        os.makedirs(simulation_wdir)

    create_env_simulations(mesh, simulation_wdir, original_name, nameSim)
    simulation = simulation_wdir + "/" + nameSim + ".sld.dat"
    with open(simulation, 'w') as f2:
        with open(template, 'r') as f:
            filedata = f.read()
            for i in range(len(variables)):
                item = variables[i]
                for name, bound in item.items():
                    filedata = filedata.replace("%" + name + "%", str(bound))
            f2.write(filedata)
            f.close()
        f2.close()
    return


@task(returns=1)
def prepare_fie(prepare_args, variables, **kwargs):
    template = prepare_args.get("template_dom")
    simulation_wdir = prepare_args.get("simulation_wdir")
    nameSim = prepare_args.get("nameSim")
    simulation = simulation_wdir + "/" + nameSim + ".fie.dat"
    with open(simulation, 'w') as f2:
        with open(template, 'r') as f:
            filedata = f.read()
            for i in range(len(variables)):
                item = variables[i]
                for name, bound in item.items():
                    filedata = filedata.replace("%" + name + "%", str(bound))
            f2.write(filedata)
            f.close()
        f2.close()
    return


@task(returns=1)
def prepare_dom(prepare_args, **kwargs):
    template = prepare_args.get("template_dom")
    mesh = prepare_args.get("mesh")
    simulation_wdir = prepare_args.get("simulation_wdir")
    nameSim = prepare_args.get("nameSim")
    simulation = simulation_wdir + "/" + nameSim + ".dom.dat"
    with open(simulation, 'w') as f2:
        with open(template, 'r') as f:
            filedata = f.read()
            filedata = filedata.replace("%sim_num%", str(nameSim))
            filedata = filedata.replace("%data_folder%", str(mesh))
            f2.write(filedata)
            f.close()
        f2.close()
    return


def get_names(prepare_args):
    problem = prepare_args.get("problem")
    variables = problem.get("variables-sampler")
    names = []
    for item in variables:
        for key, value in item.items():
            names.append(key)
    return names


def copy(src_dir, src_name, tgt_dir, tgt_name):
    src_file = os.path.join(src_dir, src_name)
    tgt_file = os.path.join(tgt_dir, tgt_name)
    shutil.copyfile(src_file, tgt_file)
    return


def create_env_simulations(mesh, sim_dir, original_name, nameSim):
    copy(mesh, original_name + ".ker.dat", sim_dir, nameSim + ".ker.dat")
    copy(mesh, original_name + ".dat", sim_dir, nameSim + ".dat")
    copy(mesh, original_name + ".dom.dat", sim_dir, nameSim + ".dom.dat")
    copy(mesh, original_name + ".fie.dat", sim_dir, nameSim + ".fie.dat")
    copy(mesh, original_name + ".post.alyadat", sim_dir, nameSim + ".post.alyadat")
    return


def callEval(parameter, variables):
    groups = re.split(r'\b', parameter)
    for group in groups:
        if group != "":
            if not group.isnumeric():
                for variable in variables:
                    if group in variable:
                        var = variable.get(group)
                        parameter = parameter.replace(group, str(var))
                        break
    res = eval(parameter)
    return res


def loop(parameter, variables):
    for variable in variables:
        if parameter in variable:
            var = variable.get(parameter)
            return var
