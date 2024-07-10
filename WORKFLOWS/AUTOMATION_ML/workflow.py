from pycompss.api.api import compss_wait_on
from PHASES.utils import phase
from PHASES.AUTOMATION_ML import check_license

def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    check_license_run=check_license()
    if check_license_run:
        print("CHECK LICENSE DONE")
        out2 = phase.run(phases.get("Simulation"), inputs, outputs, parameters, data_folder, locals())
    else:
        print("LICENSE IS NOT RUNNING!")
    return


