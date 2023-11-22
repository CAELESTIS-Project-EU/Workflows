from PHASES.SENSITIVITY import sensitivity as sens
from PHASES.SIMULATIONS import simulation as sim
from PHASES.BEFORESIMULATION import parserSimulation as parserSim
from PHASES.POSTSIMULATION import postSimulation as postSimulation
from PHASES.SAMPLERS import sampler
from pycompss.api.api import compss_wait_on
import os
import yaml


def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases = data.get("phases")
        workflow_execution(phases.get("sampler"), phases.get("sim"), phases.get("sens"), data.get("problem"),
                           execution_folder, data.get("outputs"), data.get("input"), data_folder)
    return


def workflow_execution(samplerData, simType, sensType, problem, execution_folder, outputs, input_yaml, data_folder):
    problemDef = sampler.problem_def(samplerData.get("name"), problem)
    param_values = sampler.sampler(samplerData.get("name"), problemDef, parameters=samplerData.get("parameters"))
    param_values = compss_wait_on(param_values)
    names = sampler.get_names(samplerData.get("name"), problem)
    mesh_source, templateSld, templateDom = get_input(input_yaml, data_folder)
    parent_directory, original_name = os.path.split(mesh_source)
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    y = []
    for i in range(len(param_values)):
        simulation_wdir = execution_folder + "/SIMULATIONS/" + original_name + "-s" + str(i) + "/"
        if not os.path.isdir(simulation_wdir):
            os.makedirs(simulation_wdir)
        nameSim = original_name + "-s" + str(i)
        values = param_values[i, :]
        type_sim = simType.get("type")
        variables = sampler.vars_func(samplerData.get("name"), problem, values, problem.get("variables-fixed"), names)

        out1 = parserSim.prepare_data(type_sim, mesh_source, templateSld, simulation_wdir, original_name, nameSim,
                                      variables)
        out3 = parserSim.prepare_dom_file(type_sim, templateDom, simulation_wdir, nameSim, mesh_source, out1)
        out = sim.run_sim(type_sim, simulation_wdir, nameSim, out3=out3)
        new_y = postSimulation.collect(type_sim, simulation_wdir, nameSim, out)
        y.append(new_y)
    postSimulation.write_file(type_sim, results_folder, y, outputs=outputs)
    out5 = sens.analysis(problemDef, y, results_folder, param_values, parameters=sensType, paramSampling=samplerData,
                         outputs=outputs)
    # new code
    # res= sens.generate_path(samplerData.get("name"), results_folder, outputs, out5)
    return


def get_input(input_yaml, data_folder):
    mesh = input_yaml.get("mesh", [])
    mesh_folder = ""
    for item in mesh:
        if isinstance(item, dict) and 'path' in item:
            mesh_folder = item['path']
            break  # Exit the loop after finding the first 'folder'

    template_sld = input_yaml.get("template_sld", [])
    templateSld_folder = ""
    for item in template_sld:
        if isinstance(item, dict) and 'path' in item:
            templateSld_folder = item['path']
            break  # Exit the loop after finding the first 'folder'

    template_dom = input_yaml.get("template_dom", [])
    templateDom_folder = ""
    for item in template_dom:
        if isinstance(item, dict) and 'path' in item:
            templateDom_folder = item['path']
            break  # Exit the loop after finding the first 'folder'

    # Now use these folder paths as needed
    mesh_source = os.path.join(data_folder, mesh_folder) if mesh_folder else None
    templateSld = os.path.join(data_folder, templateSld_folder) if templateSld_folder else None
    templateDom = os.path.join(data_folder, templateDom_folder) if templateDom_folder else None
    return mesh_source, templateSld, templateDom