import importlib

def run_sim(type_sim, wdir, name, **kwargs):
    module = importlib.import_module('PHASES.SIMULATIONS.' + type_sim)
    return getattr(module, 'simulation')(wdir, name, **kwargs)

