import os

from pycompss.api.api import compss_wait_on
from PHASES.utils import phase
from PHASES.AUTOMATION_ML import check_license

def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    df, DoE_names= phase.run(phases.get("Sampling"), inputs, outputs, parameters, data_folder, locals())
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    check_license_run=check_license.check_license()
    df = compss_wait_on(df)
    DoE_names = compss_wait_on(DoE_names)
    if check_license_run:
        print("CHECK LICENSE DONE")
        a = 0
        for index, row in df.iterrows():
            a += 1
            line_number = 'line' + str(a)
            DoE_line = dict(zip(DoE_names, row))
            phase.run(phases.get("Simulation"), inputs, outputs, parameters, data_folder, locals())
    else:
        print("LICENSE IS NOT RUNNING!")
    return


