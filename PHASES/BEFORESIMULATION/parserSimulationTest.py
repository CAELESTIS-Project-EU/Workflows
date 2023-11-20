import importlib
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(sim_dir=DIRECTORY_INOUT)
def prepare_data(type_sim, wdir, template, sim_dir, original_name, nameSim, variables):
    print("TYPE: ", type_sim)
    module = importlib.import_module('PHASES.BEFORESIMULATION.' + type_sim)
    getattr(module, 'parser')(variables, wdir, template, sim_dir, original_name, nameSim)


@task(sim_dir=DIRECTORY_INOUT)
def prepare_fie_file(type_sim, template, sim_dir, nameSim, variables, wdir, original_name):
    print("TYPE: ", type_sim)
    module = importlib.import_module('PHASES.BEFORESIMULATION.' + type_sim)
    getattr(module, 'parser_fie')(variables, template, sim_dir, nameSim, wdir, original_name)


@task(sim_dir=DIRECTORY_INOUT)
def prepare_dom_file(type_sim, template, sim_dir, nameSim):
    print("TYPE: ", type_sim)
    module = importlib.import_module('PHASES.BEFORESIMULATION.' + type_sim)
    getattr(module, 'parser_dom')(sim_dir, nameSim, template)


