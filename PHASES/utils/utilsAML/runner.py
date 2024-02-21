from PHASES.utils.utilsAML.data import resolve_data
import importlib

def run_software(software, variables):
    if isinstance(software, list):
        for s in software:
            run_software(s, variables)
    else:
        module = importlib.import_module(software.module)
        func = getattr(module, software.function)
        params = resolve_data(software.parameters, variables)
        return func(**params)