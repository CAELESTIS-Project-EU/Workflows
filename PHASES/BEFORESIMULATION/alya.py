import importlib
import os
import re
import shutil
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.on_failure import on_failure
from pycompss.api.constraint import constraint

gen_timeout=int(os.environ.get("GEN_TIMEOUT","3600"))
gen_cores=int(os.environ.get("GEN_CORES","1"))

def prepare_data(**kwargs):
    prepare_args = kwargs
    variables = vars_func(prepare_args)
    out1 = prepare_sld(prepare_args, variables)
    bool_template_fie=check_template_exist(prepare_args,"template_fie")
    bool_template_dom=check_template_exist(prepare_args,"template_dom")
    if bool_template_fie:
        out2 = prepare_fie(prepare_args, variables, out=out1)
    if bool_template_dom:
        out3 = prepare_dom(prepare_args, out=out1)
    return out3


def prepare_data_rve_sld(**kwargs):
    prepare_args = kwargs
    variables = vars_func(prepare_args)
    out1 = prepare_rve_sld(prepare_args, variables)
    out3 = prepare_rve_dom(prepare_args, out=out1)
    return out3


def prepare_data_coupontool(**kwargs):
    prepare_args = kwargs
    variables = vars_func(prepare_args)
    out1 = prepare_coupontool(prepare_args, variables)
    return out1


def prepare_data_rvetool(**kwargs):
    prepare_args = kwargs
    variables = vars_func(prepare_args)
    out1 = prepare_rvetool(prepare_args, variables)
    return out1


def check_template_exist(element, template):
    if template in element:
        return True
    else:
        return False


@task(returns=1)
def vars_func(prepare_args):
    variables_sampled=get_value(prepare_args, "values")
    names = get_names(prepare_args)
    problem = get_value(prepare_args,"problem")
    variables_fixed = problem.get("variables-fixed")
    calls = problem.get("variables-derivate")
    variables = []
    for i in range(len(variables_sampled)):
        value = {names[i]: variables_sampled[i]}
        variables.append(value)
    for variable_fixed in variables_fixed:
        variables.append(variable_fixed)
    if calls:
        for name, value in calls.items():
            call = value
            head, tail = call.get("method").split(".")
            parameters = call.get("parameters")
            args = []
            for parameter in parameters:
                if re.search(r"eval\(", parameter):
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
    original_name_sim = get_value(prepare_args, "original_name_sim")
    template = get_value(prepare_args, "template_sld")
    mesh = get_value(prepare_args, "mesh")
    simulation_wdir = get_value(prepare_args, "simulation_wdir")
    name_sim = get_value(prepare_args,"name_sim")
    if not os.path.isdir(simulation_wdir):
        os.makedirs(simulation_wdir)
    create_env_simulations(mesh, simulation_wdir, original_name_sim, name_sim)
    simulation = simulation_wdir + "/" + name_sim + ".sld.dat"
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
def prepare_rve_sld(prepare_args, variables, **kwargs):
    original_name_sim = get_value(prepare_args, "original_name_sim")
    mesh = get_value(prepare_args, "mesh")
    simulation_wdir = get_value(prepare_args, "simulation_wdir")
    name_sim = get_value(prepare_args,"name_sim")
    cases_loads = get_value(prepare_args,"cases_loads")
    if not os.path.isdir(simulation_wdir):
        os.makedirs(simulation_wdir)
    for icase in cases_loads:
        if icase == "11":
            template = get_value(prepare_args, "template_sld11")
        elif icase == "22":
            template = get_value(prepare_args, "template_sld22")
        elif icase == "12":
            template = get_value(prepare_args, "template_sld12")
        os.makedirs(os.path.join(simulation_wdir,original_name_sim+'-'+icase))
        create_rve_env_simulations(os.path.join(mesh,original_name_sim+'-'+icase), os.path.join(simulation_wdir,original_name_sim+'-'+icase), original_name_sim+'-'+icase, original_name_sim+'-'+icase)
        simulation = os.path.join(simulation_wdir,original_name_sim+'-'+icase, original_name_sim+'-'+icase+ ".sld.dat")
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
    template = get_value(prepare_args, "template_fie")
    simulation_wdir = get_value(prepare_args, "simulation_wdir")
    original_name_sim = get_value(prepare_args, "original_name_sim")
    name_sim = get_value(prepare_args, "name_sim")
    simulation = os.path.join(simulation_wdir, name_sim + ".fie.dat")
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
    template = get_value(prepare_args, "template_dom")
    simulation_wdir = get_value(prepare_args, "simulation_wdir")
    original_name_sim = get_value(prepare_args, "original_name_sim")
    name_sim = get_value(prepare_args, "name_sim")
    mesh = get_value(prepare_args, "mesh")
    simulation = os.path.join(simulation_wdir, name_sim + ".dom.dat")
    with open(simulation, 'w') as f2:
        with open(template, 'r') as f:
            filedata = f.read()
            filedata = filedata.replace("%sim_num%", str(name_sim))
            filedata = filedata.replace("%data_folder%", str(mesh))
            f2.write(filedata)
            f.close()
        f2.close()
    return


def USECASEconvert_and_surrogate(**prepare_args):
    ########################## USECASE convert #####################
    import USECASEconvert
    input_files_folder = get_value(prepare_args, "input_files_folder")
    output_files_folder = get_value(prepare_args, "output_files_folder")
    lperm_path = get_value(prepare_args, "lperm_path")
    inp_path = get_value(prepare_args, "inp_path")
    template_path = get_value(prepare_args, "template_COUPONtool")
    mechanical_base_name = get_value(prepare_args, "Mechanical_Base_Name")
    print()
    print("prepareeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    print(prepare_args)
    print(f"Input files folder: {input_files_folder}", flush=True)
    print(f"Output files folder: {output_files_folder}", flush=True)
    print(f"lperm path: {lperm_path}, inp path: {inp_path}", flush=True)
    print(f"Template path: {template_path}", flush=True)
    print(f"Mechanical Base Name: {mechanical_base_name}", flush=True)

    # Look for the proper .lperm and .inp files ({case_number}.lperm, {case_number}.inp)
    case_number = int(get_value(prepare_args, "index")) + 1
    print(f"Case number (index+1): {case_number}", flush=True)

    # Finding .lperm file
    lperm_file_path = None
    files = os.listdir(lperm_path)
    print(f"Files in lperm path: {files}", flush=True)
    for file in files:
        if file.endswith(str(case_number) + '.lperm'):
            lperm_file_path = os.path.join(input_files_folder, file)
            print(f"Found lperm file: {lperm_file_path}", flush=True)
            break
    else:
        print("No matching .lperm file found", flush=True)

    # Finding .inp file
    inp_file_path = None
    files = os.listdir(inp_path)
    print(f"Files in inp path: {files}", flush=True)
    for file in files:
        if file.endswith(str(case_number) + '.inp'):
            inp_file_path = os.path.join(input_files_folder, file)
            print(f"Found inp file: {inp_file_path}", flush=True)
            break
    else:
        print("No matching .inp file found", flush=True)

    # Modify the template
    execution_folder = get_value(prepare_args, "execution_folder")
    modified_template_path = os.path.join(execution_folder, "templates",
                                          "inputs_USECASE_convert.yaml")
    print(f"Modified template path: {modified_template_path}", flush=True)

    if not os.path.isdir(modified_template_path):
        os.makedirs(modified_template_path)
        print(f"Created directory: {modified_template_path}", flush=True)

    with open(modified_template_path, 'w') as f2:
        with open(template_path, 'r') as f:
            filedata = f.read()
            filedata = filedata.replace("%lperm_file_path%",
                                        str(lperm_file_path))
            filedata = filedata.replace("%inp_file_path%", str(inp_file_path))
            filedata = filedata.replace("%output_path%",
                                        str(output_files_folder))
            filedata = filedata.replace("%JobName%", str(mechanical_base_name))
            f2.write(filedata)
            print(f"Modified template content written in path {modified_template_path}", flush=True)
            print(filedata, flush=True)
            f.close()
        f2.close()

    USECASEconvert.runUSECASEconvert(modified_template_path)
    print("USECASEconvert executed", flush=True)

    ########################## SURROGATE #######################
    return


@task(returns=1)
def prepare_rve_dom(prepare_args, **kwargs):
    simulation_wdir = get_value(prepare_args, "simulation_wdir")
    original_name_sim = get_value(prepare_args, "original_name_sim")
    name_sim = get_value(prepare_args, "name_sim")
    mesh = get_value(prepare_args, "mesh")
    cases_loads = get_value(prepare_args,"cases_loads")
    for icase in cases_loads:
        if icase == "11":
            template = get_value(prepare_args, "template_dom11")
        elif icase == "22":
            template = get_value(prepare_args, "template_dom22")
        elif icase == "12":
            template = get_value(prepare_args, "template_dom12")
        simulation_folder = os.path.join(simulation_wdir,original_name_sim+'-'+icase)
        simulation = simulation_folder + "/" + original_name_sim + '-' + icase + ".dom.dat"
        with open(simulation, 'w') as f2:
            with open(template, 'r') as f:
                filedata = f.read()
                filedata = filedata.replace("%sim_num%", str(name_sim))
                filedata = filedata.replace("%data_folder%", str(mesh))
                f2.write(filedata)
                f.close()
            f2.close()
    return


@constraint(computing_units=gen_cores)
@task(returns=1, on_failure="CANCEL_SUCCESSORS", time_out=gen_timeout )
def prepare_coupontool(prepare_args, variables):
    from coupontool import COUPONtool
    template = get_value(prepare_args, "template_coupontool")
    simulation_wdir = get_value(prepare_args, "simulation_wdir")
    name_sim = get_value(prepare_args, "name_sim")
    simulation = simulation_wdir + "/" + name_sim + '.py'
    if not os.path.isdir(simulation_wdir):
        os.makedirs(simulation_wdir)
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
    COUPONtool.runCOUPONtool(simulation, name_sim, simulation_wdir, 'open-hole', debug=False)
    return

@constraint(computing_units=gen_cores)
@task(returns=1, on_failure="CANCEL_SUCCESSORS", time_out=gen_timeout )
def prepare_rvetool(prepare_args, variables):
    import RVEtool
    template = get_value(prepare_args, "template_rvetool")
    simulation_wdir = get_value(prepare_args, "simulation_wdir")
    name_sim = get_value(prepare_args, "name_sim")
    simulation = simulation_wdir + "/" + name_sim + '.yaml'
    if not os.path.isdir(simulation_wdir):
        os.makedirs(simulation_wdir)
    with open(simulation, 'w') as f2:
        with open(template, 'r') as f:
            filedata = f.read()
            for i in range(len(variables)):
                item = variables[i]
                for name, bound in item.items():
                    filedata = filedata.replace("%" + name + "%", str(bound))
            filedata = filedata.replace("%JobName%", str(name_sim))
            output_path = os.path.split(os.path.normpath(simulation_wdir))[0]
            filedata = filedata.replace("%output_path%", output_path)
            f2.write(filedata)
            f.close()
        f2.close()
    RVEtool.runRVEtool(simulation)
    return


def get_value(element, param):
    if param in element:
        return element[param]
    else:
        raise ValueError(f"The key '{param}' was not found in the dictionary.")


def get_names(prepare_args):
    problem = get_value(prepare_args, "problem")
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


def create_env_simulations(mesh, sim_dir, original_name, name_sim):
    copy(mesh, original_name + ".ker.dat", sim_dir, name_sim + ".ker.dat")
    copy(mesh, original_name + ".dat", sim_dir, name_sim + ".dat")
    copy(mesh, original_name + ".dom.dat", sim_dir, name_sim + ".dom.dat")
    copy(mesh, original_name + ".fie.dat", sim_dir, name_sim + ".fie.dat")
    copy(mesh, original_name + ".post.alyadat", sim_dir, name_sim + ".post.alyadat")
    return


def create_rve_env_simulations(mesh, sim_dir, original_name, name_sim):
    copy(mesh, original_name + ".ker.dat", sim_dir, name_sim + ".ker.dat")
    copy(mesh, original_name + ".dat", sim_dir, name_sim + ".dat")
    copy(mesh, original_name + ".dom.dat", sim_dir, name_sim + ".dom.dat")
    copy(mesh, original_name + ".post.alyadat", sim_dir, name_sim + ".post.alyadat")
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
