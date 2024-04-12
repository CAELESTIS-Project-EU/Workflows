from pycompss.api.api import compss_wait_on
from PHASES.utils import phase


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    out1 = phase.run(phases.get("Preprocess"), inputs, outputs, parameters, data_folder, locals())
    out1=compss_wait_on(out1)
    out2 = phase.run(phases.get("Simulation"), inputs, outputs, parameters, data_folder, locals())
    out2 = compss_wait_on(out2)
    return


