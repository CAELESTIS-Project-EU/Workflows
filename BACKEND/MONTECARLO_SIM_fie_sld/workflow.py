from PHASES.SAMPLERS import sampler
from PHASES.SIMULATIONS import simulation as sim
from PHASES.POSTSIMULATION import postSimulation
from PHASES.BEFORESIMULATION import parserSimulation as parserSim
from pycompss.api.api import compss_wait_on
import os
import yaml


def workflow(path, execution_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases = data.get("phases")
        workflow_execution(phases.get("sampler"), data.get("problem"), execution_folder, data.get("input"),
                           phases.get("sim"), data.get("outputs"))
    return


def workflow_execution(samplerData, problem, execution_folder, input, simType, outputs):
    sample_set = sampler.sampler(samplerData.get("name"), problem)
    sample_set = compss_wait_on(sample_set)
    matrix_fie = sampler.sampler_fie(samplerData.get("name"), problem)
    matrix_fie = compss_wait_on(matrix_fie)
    mesh = input.get("mesh")
    templateSld = input.get("template_sld")
    templateFie = input.get("template_fie")
    type_sim = simType.get("type")
    parent_directory, original_name = os.path.split(mesh)
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    y = []
    for i in range(len(sample_set)):
        simulation_wdir = execution_folder + "/SIMULATIONS/" + original_name + "-s" + str(i) + "/"
        if not os.path.isdir(simulation_wdir):
            os.makedirs(simulation_wdir)
        nameSim = original_name + "-s" + str(i)
        sample_fie = matrix_fie[i, :]
        values = sample_set[i, :]
        variables_sld = sampler.vars_func_sld(samplerData.get("name"), problem, values, problem.get("variables-fixed"))
        variables_fie = sampler.vars_func_fie(samplerData.get("name"), problem, sample_fie)
        parserSim.prepare_data(type_sim, mesh, templateSld, simulation_wdir, original_name, nameSim, variables_sld)
        parserSim.prepare_fie_file(type_sim, templateFie, simulation_wdir, nameSim, variables_fie)
        sim.run_sim(type_sim, simulation_wdir, nameSim)
        new_y = postSimulation.collect(type_sim, simulation_wdir, nameSim)
        y.append(new_y)
    postSimulation.write_file(type_sim, results_folder, y, outputs=outputs)
    return
