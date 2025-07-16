import os
import numpy as np

from PHASES.utils import phase
from PHASES.utils import check_license

from pycompss.api.api import compss_wait_on
from pycompss.api.task import task
from pycompss.api.parameter import *
PAM_NP = 24

def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    global PAM_NP
    import time
    if "PAM_NP" in parameters:
        PAM_NP=int(parameters["PAM_NP"])
        print("Setting PAM NP to " + str(PAM_NP))
    #
    # Sampling and results folder
    #
    df, DoE_names = phase.run(phases.get("Sampling"), inputs, outputs, parameters, data_folder, locals())
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    df = compss_wait_on(df)
    DoE_names = compss_wait_on(DoE_names)
    #
    # Check license
    # 
    check_license_run = check_license.check_license()
    if check_license_run:
        print("CHECK LICENSE DONE")
        a = 0
        #
        # DoE
        # 
        for index, row in df.iterrows():
            a += 1
            line_number = 'line' + str(a)
            row_folder = os.path.join(results_folder, line_number)
            if not os.path.isdir(row_folder):
                os.makedirs(row_folder)
            DoE_line = dict(zip(DoE_names, row))
            #
            # PAM-COMPOSITES simulations
            # 
            sim_out = phase.run(phases.get("PAM-COMPOSITE_Simulations"), inputs, outputs, parameters, data_folder, locals())
            # 
            # Postprocess PAM-COMPOSITES simulations
            #
            if "PAM-COMPOSITE_PostProcess" in phases:
                phase.run(phases.get("PAM-COMPOSITE_PostProcess"), inputs, outputs, parameters, data_folder, locals(), out=sim_out)
    else:
        print("LICENSE IS NOT RUNNING!")
    return

