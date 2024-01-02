from pycompss.api.mpi import mpi
from pycompss.api.task import task
from pycompss.api.parameter import *
@mpi(runner="mpirun", binary="$ALYA_BIN", args="{{name}} ", processes="$ALYA_PROCS", processes_per_node="$ALYA_PPN", working_dir="{{wdir}}")
@task(returns=1, time_out=3600)
def simulation(wdir, name, **kwargs):
        cpus=64
        if kwargs.get("sim_params"):
                sim_params = kwargs.get("sim_params")
                cpus= int(sim_params.get("cpus", 64))
        return