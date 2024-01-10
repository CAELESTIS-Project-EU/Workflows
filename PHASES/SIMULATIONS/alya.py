from pycompss.api.mpi import mpi
from pycompss.api.task import task
from pycompss.api.parameter import *
@mpi(runner="mpirun", binary="$ALYA_BIN", args="{{nameSim}}", processes="$ALYA_PROCS", processes_per_node="$ALYA_PPN", working_dir="{{simulation_wdir}}")
@task(returns=1, time_out=3600)
def simulation(nameSim, simulation_wdir, **kwargs):
        return

