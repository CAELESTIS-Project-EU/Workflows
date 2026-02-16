import os
import sys

import yaml
import importlib
from PHASES.utils import phase as phase


def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        workflow_type=data.get("workflow_type")
        parameters=data.get("parameters")
        os.environ["PAM_NP"] = str(parameters.get("PAM_NP", "1"))  # Default to 1 if not set
        inputs=data.get("inputs")
        outputs = data.get("outputs")
        phases = data.get("phases")
        module_call, function_call = phase.split_string_at_last_dot(workflow_type)
        module = importlib.import_module(module_call)
        getattr(module, function_call)(execution_folder, data_folder, phases, inputs, outputs, parameters)
    return



if __name__ == '__main__':
    path = str(sys.argv[1])
    execution_folder = str(sys.argv[2])
    data_folder = str(sys.argv[3])
    workflow(path, execution_folder, data_folder)
