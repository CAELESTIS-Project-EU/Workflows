import importlib
from pycompss.api.task import task
from pycompss.api.parameter import *

@task(returns=1)
def prepare_data(type_sim, wdir, template, sim_dir, original_name, nameSim, variables):
    print("TYPE: ", type_sim)
    module = importlib.import_module('PHASES.BEFORESIMULATION.' + type_sim)
    return getattr(module, 'parser')(variables, wdir, template, sim_dir, original_name, nameSim)

@task(returns=1)
def prepare_fie_file(type_sim, template, sim_dir, nameSim, variables, wdir, original_name, out):
    print("TYPE: ", type_sim)
    module = importlib.import_module('PHASES.BEFORESIMULATION.' + type_sim)
    return getattr(module, 'parser_fie')(variables, template, sim_dir, nameSim, wdir, original_name)

@task(returns=1)
def prepare_dom_file(type_sim, template, data_folder, nameSim, mesh_source, out):
    print("TYPE: ", type_sim)
    module = importlib.import_module('PHASES.BEFORESIMULATION.' + type_sim)
    return getattr(module, 'parser_dom')(data_folder, nameSim, template, mesh_source)