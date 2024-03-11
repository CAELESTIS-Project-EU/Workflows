#from pycompss.api.api import compss_wait_on
from PHASES.utils.utilsAML import args_values_AML, phase_AML

import os


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    prepare_out = phase_AML.run(args_values_AML.get_values(phases.get("postSIM"), inputs, outputs, parameters, data_folder, locals()))
    prepare_out = phase_AML.run(args_values_AML.get_values(phases.get("simulation"), inputs, outputs, parameters, data_folder, locals()))
    return


def get_parameters_phase(parametersPhase):
    parameters={}
    for key,value in parametersPhase.items():
        value=value.get_value()
        parameters[key]=value
    return parameters