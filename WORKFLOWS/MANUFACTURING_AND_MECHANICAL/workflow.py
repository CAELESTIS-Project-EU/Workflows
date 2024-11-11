import os

from pycompss.api.api import compss_wait_on
from PHASES.utils import phase
from PHASES.AUTOMATION_ML import check_license
PAM_NP = 1


def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    global PAM_NP
    import time
    if "PAM_NP" in parameters:
        PAM_NP=int(parameters["PAM_NP"])
        print("Setting PAM NP to " + str(PAM_NP))
    df, DoE_names= phase.run(phases.get("Sampling"), inputs, outputs, parameters, data_folder, locals())
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    #check_license_run=check_license.check_license()
    check_license_run = True
    df = compss_wait_on(df)
    DoE_names = compss_wait_on(DoE_names)
    if check_license_run:
        print("CHECK LICENSE DONE")
        a = 0
        for index, row in df.iterrows():
            a += 1
            line_number = 'line' + str(a)
            simulation_wdir = os.path.join(execution_folder, "SIMULATIONS", line_number)
            if not os.path.isdir(simulation_wdir):
                os.makedirs(simulation_wdir)
            DoE_line = dict(zip(DoE_names, row))
            phase.run(phases.get("Simulation"), inputs, outputs, parameters, data_folder, locals())
            t1 = time.time()
            phase.run(phases.get("Prepare Data"), inputs, outputs, parameters,
                      data_folder, locals(), index=index, row_folder=simulation_wdir)
            print ("TIMEEEEEEEEEE:", time.time() - t1)
            phase.run(phases.get("Simulation2"), inputs, outputs, parameters,
                      data_folder, locals())
            if "PostProcess" in phases:
                phase.run(phases.get("PostProcess"), inputs, outputs, parameters, data_folder, locals())

    else:
        print("LICENSE IS NOT RUNNING!")
    return


