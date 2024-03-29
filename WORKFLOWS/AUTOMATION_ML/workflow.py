from pycompss.api.api import compss_wait_on
from PHASES.utils import phase


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    out1 = phase.run(phases.get("postSIM"), inputs, outputs, parameters, data_folder, locals())
    out1=compss_wait_on(out1)
    print(out1)
    out2 = phase.run(phases.get("simulation"), inputs, outputs, parameters, data_folder, locals())
    out2 = compss_wait_on(out2)
    print(out2)
    return


def get_parameters_phase(parametersPhase):
    parameters={}
    for key,value in parametersPhase.items():
        value=value.get_value()
        parameters[key]=value
    return parameters