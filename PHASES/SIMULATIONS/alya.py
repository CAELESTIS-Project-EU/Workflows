from pycompss.api.mpi import mpi
from pycompss.api.task import task
from pycompss.api.parameter import *


@mpi(runner="mpirun", binary="$ALYA_BIN", args="{{name_sim}}", processes="$ALYA_PROCS", processes_per_node="$ALYA_PPN", working_dir="{{simulation_wdir}}")
@task(returns=1, time_out=3600)
def simulation(name_sim, simulation_wdir, **kwargs):
    return


