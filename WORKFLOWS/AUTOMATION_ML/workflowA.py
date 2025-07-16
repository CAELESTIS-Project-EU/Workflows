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
    #
    # Sampling and results folder
    #
    sample_set, DoE_names = phase.run(phases.get("Sampling"), inputs, outputs, parameters, data_folder, locals())
    sample_set = compss_wait_on(sample_set)
    DoE_names = compss_wait_on(DoE_names)
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    # Check license
    check_license_run = check_license.check_license()
    if check_license_run:
        for index, row in sample_set.iterrows():
            line_number = 'line' + str(index+1)
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
            phase.run(phases.get("PAM-COMPOSITE_PostProcess"), inputs, outputs, parameters, data_folder, locals(), out=sim_out)
    else:
        print("LICENSE IS NOT RUNNING!")
    return
