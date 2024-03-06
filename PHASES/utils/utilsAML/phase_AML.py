import importlib


def run(module_call, function, phase_args, **kwargs):
    # Assuming phase_info is a tuple (phase_function, phase_args)
    module = importlib.import_module(module_call)
    return getattr(module, function)(**phase_args, **kwargs)
