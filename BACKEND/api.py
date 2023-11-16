import yaml
import sys
import importlib


def workflow(path, execution_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        workflow_type=data.get("workflow_type")
        module = importlib.import_module('BACKEND.'+workflow_type+'.workflow')
        getattr(module, 'workflow')(path, execution_folder, data_folder)
    return

if __name__ == '__main__':
    path=str(sys.argv[1])
    execution_folder=str(sys.argv[2])
    data_folder = str(sys.argv[3])
    workflow(path, execution_folder, data_folder)


