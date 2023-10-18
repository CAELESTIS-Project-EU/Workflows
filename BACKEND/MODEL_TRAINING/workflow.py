from PHASES.SAMPLERS import PYDOE,sampler
from PHASES.SIMULATIONS import simulation as sim
from PHASES.POSTSIMULATION import postSimulation
from PHASES.BEFORESIMULATION import parserSimulation as parserSim
from PHASES.MODEL_TRAINING import trainingModel
#from pycompss.api.api import compss_wait_on
import os
import yaml

def workflow(path, execution_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases=data.get("phases")
        model_creation(phases.get("sampler"),phases.get("training"), data.get("outputs"), data.get("problem"), execution_folder, data.get("input"),  phases.get("sim"))
    return

def model_creation(samplerData, training, outputs, problem,execution_folder,input, simType):
    sample_set= sampler.sampler(samplerData.get("name"), problem, parameters= samplerData.get("parameters"))
    mesh = input.get("mesh")
    template = input.get("template")
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
        values = sample_set[i, :]
        type_sim = simType.get("type")
        variables=sampler.vars_func(samplerData.get("name"),problem,values,problem.get("variables-fixed"))
        parserSim.prepare_data(type_sim, mesh, template, simulation_wdir, original_name, nameSim, variables)
        sim.run_sim(type_sim, simulation_wdir, nameSim)
        new_y = postSimulation.collect(type_sim, simulation_wdir, nameSim)
        y.append(new_y)
    trainingModel.training(sample_set, y)
    return