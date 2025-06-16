from pycompss.api.api import compss_wait_on
from PHASES.utils import phase


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    sample_set = phase.run(phases.get("read_doe"), inputs, outputs, parameters, data_folder, locals())
    for i in range(sample_set.shape[0]):
        PAM_RTMf = phase.run(phases.get("PAM_RTMf"), inputs, outputs, parameters, data_folder, locals())
        PAM_RTMc = phase.run(phases.get("PAM_RTMc"), inputs, outputs, parameters, data_folder, locals())
        PAM_DISTORTION = phase.run(phases.get("PAM_DISTORTION"), inputs, outputs, parameters, data_folder, locals())
    return