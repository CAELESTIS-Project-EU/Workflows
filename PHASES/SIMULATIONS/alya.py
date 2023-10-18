from PHASES import configuration as cfg
from pycompss.api.mpi import mpi
from pycompss.api.task import task
from pycompss.api.parameter import *
@mpi(runner="mpirun", binary="$ALYA_BIN", args="{{name}} ", processes="$ALYA_PROCS", processes_per_node="$ALYA_PPN", working_dir="{{wdir}}")
@task(returns=1, time_out=3600)
def simulation(wdir, name, **kwargs):
        return