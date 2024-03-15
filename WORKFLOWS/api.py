import os
import sys

import yaml
import importlib
from PHASES.utils import parserAML, phase as phase
from PHASES.utils.utilsAML import xml_to_yaml


def workflow(path, execution_folder, data_folder):
    extension=get_file_extension(path)
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        workflow_type=data.get("workflow_type")
        parameters=data.get("parameters")
        inputs=data.get("inputs")
        outputs = data.get("outputs")
        phases = data.get("phases")
        module_call, function_call = phase.split_string_at_last_dot(workflow_type)
        module = importlib.import_module(module_call)
        getattr(module, function_call)(execution_folder, data_folder, phases, inputs, outputs, parameters)
    return


def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension

if __name__ == '__main__':
    path = "/home/rcecco/BSCprojects/templates_yaml/AML/multiple_chain.yaml"
    execution_folder = "/home/rcecco/BSCprojects/templates_yaml/MONTECARLO_sld/OHT_Validation_D2.yaml"
    data_folder = "/home/rcecco/BSCprojects/templates_yaml/MONTECARLO_sld/OHT_Validation_D2.yaml"
    workflow(path, execution_folder, data_folder)
