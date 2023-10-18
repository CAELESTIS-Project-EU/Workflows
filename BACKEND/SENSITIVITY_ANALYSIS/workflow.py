from PHASES.SENSITIVITY import sensitivity as sens
from PHASES.SIMULATIONS import simulation as sim
#from PHASES.POSTSIMULATION import postSimulation
#from PHASES.BEFORESIMULATION import parserSimulation as parserSim
from PHASES.BEFORESIMULATION import parserSimulationTest as parserSim
from PHASES.POSTSIMULATION import postSimulationtest as postSimulation
from PHASES.SAMPLERS import sampler
from pycompss.api.api import compss_wait_on
import os
import yaml

def workflow(path, execution_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases=data.get("phases")
        workflow_execution(phases.get("sampler"), phases.get("sim"), phases.get("sens"), data.get("problem"), execution_folder, data.get("outputs"), data.get("input"))
    return

def workflow_execution(samplerData, simType, sensType, problem, execution_folder, outputs, input):
    problemDef = sampler.problem_def(samplerData.get("name"),problem)
    param_values = sampler.sampler(samplerData.get("name"), problemDef, parameters= samplerData.get("parameters"))
    param_values= compss_wait_on(param_values)
    names = sampler.get_names(samplerData.get("name"), problem)
    print(names)
    mesh=input.get("mesh")
    template=input.get("template_sld")
    templateDom = input.get("template_dom")
    parent_directory, original_name = os.path.split(mesh)
    results_folder=execution_folder+"/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    y=[]
    for i in range(len(param_values)):
        simulation_wdir = execution_folder+"/SIMULATIONS/"+original_name+"-s"+str(i)+"/"
        if not os.path.isdir(simulation_wdir):
            os.makedirs(simulation_wdir)
        nameSim= original_name+"-s"+str(i)
        values= param_values[i, :]
        type_sim=simType.get("type")
        variables=sampler.vars_func(samplerData.get("name"),problem,values,problem.get("variables-fixed"), names)

        out1 = parserSim.prepare_data(type_sim, mesh, template, simulation_wdir, original_name, nameSim,
                                      variables)
        out3 = parserSim.prepare_dom_file(type_sim, templateDom, simulation_wdir, nameSim, out1)
        out = sim.run_sim(type_sim, simulation_wdir, nameSim, out3=out3)
        new_y = postSimulation.collect(type_sim, simulation_wdir, nameSim, out)
        """parserSim.prepare_data(type_sim, mesh, template, simulation_wdir, original_name, nameSim, variables)
        parserSim.prepare_dom_file(type_sim, templateDom, simulation_wdir, nameSim)
        sim.run_sim(type_sim, simulation_wdir, nameSim)
        new_y=postSimulation.collect(type_sim,simulation_wdir, nameSim)"""
        y.append(new_y)
    out5= sens.analysis(problemDef, y, results_folder, param_values,  parameters= sensType, paramSampling=samplerData, outputs=outputs)
    # res= sens.generate_path(samplerData.get("name"), results_folder, outputs, out5)
    return
