import yaml
import sys
import importlib
import PHASES.utils.phase as phase

def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        workflow_type=data.get("workflow_type")
        parameters=data.get("parameters")
        module_call, function_call = phase.split_string_at_last_dot(workflow_type)
        module = importlib.import_module(module_call)
        getattr(module, function_call)(data, execution_folder, data_folder, parameters)
    return

if __name__ == '__main__':
    path = str(sys.argv[1])
    execution_folder = str(sys.argv[2])
    data_folder = str(sys.argv[3])
    workflow(path, execution_folder, data_folder)


