#from pycompss.api.api import compss_wait_on
from PHASES.utils import args_values, phase
from PHASES.utils.utilsAML import args_values_AML, phase_AML

import os


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    for phase in phases.values():
        for i in range(len(phase)):
            p=phase[i]
            function=p.get_function()
            module = p.get_module()
            parameterPhase = get_parameters_phase(p.get_parameters())
            args_dict=args_values_AML.get_values(parameterPhase, inputs, outputs, parameters, data_folder, locals())
            phase_AML.run(module, function, args_dict)
    return


def get_parameters_phase(parametersPhase):
    parameters={}
    for key,value in parametersPhase.items():
        value=value.get_value()
        parameters[key]=value
    return parameters