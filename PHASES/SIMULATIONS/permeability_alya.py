import os.path

from pycompss.api.mpi import mpi
from pycompss.api.task import task
from pycompss.api.parameter import *


@mpi(runner="mpirun", binary="$ALYA_BIN", args="{{case_name}}", processes="$ALYA_PROCS", processes_per_node="$ALYA_PPN", working_dir="{{simulation_wdir}}")
@task(returns=1, time_out=3600)
def simulation(case_name, simulation_wdir, **kwargs):
    return


def alya_simulation(case_name, simulation_wdir, cases_permeability, **kwargs):
    for case in cases_permeability:
        simulation_wdir_case=os.path.join(simulation_wdir, case)
        simulation(case_name,simulation_wdir_case)
    return