import os

import yaml
import sys
import importlib
from PHASES.utils import parserAML, phase as phase


def workflow(path, execution_folder, data_folder):
    extension=get_file_extension(path)
    if extension==".yaml":
        with open(path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            workflow_type=data.get("workflow_type")
            parameters=data.get("parameters")
            inputs=data.get("inputs")
            outputs = data.get("inputs")
            phases = data.get("phases")
            module_call, function_call = phase.split_string_at_last_dot(workflow_type)
            module = importlib.import_module(module_call)
            getattr(module, function_call)(execution_folder, data_folder, phases, inputs, outputs, parameters)
    elif extension==".aml" or extension==".xml":
            AMLdoc= parserAML.AutomationMLDocument(path)
            AMLdoc.parse()
            print("DOCUMENT")
            print(AMLdoc)
    return


def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension

if __name__ == '__main__':
    path = "/home/rcecco/BSCprojects/templates_yaml/AML/multiple_chain.xml"
    execution_folder = "/home/rcecco/BSCprojects/testCODE/"
    data_folder = "/home/rcecco/BSCprojects/testCODE/"
    """path = str(sys.argv[1])
    execution_folder = str(sys.argv[2])
    data_folder = str(sys.argv[3])"""
    workflow(path, execution_folder, data_folder)


