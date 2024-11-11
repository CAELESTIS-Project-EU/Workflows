from pycompss.api.mpi import mpi
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.on_failure import on_failure
import os

alya_procs=int(os.environ.get("ALYA_PROCS", "3"))
alya_ppn=int(os.environ.get("ALYA_PPN", "3"))
alya_timeout=int(os.environ.get("ALYA_TIMEOUT", "3600"))
if alya_procs < alya_ppn:
    alya_ppn=alya_procs

@on_failure(management='IGNORE')
@mpi(runner="mpirun", binary="$ALYA_BIN", args="{{name_sim}}", processes=alya_procs, processes_per_node=alya_ppn, working_dir="{{simulation_wdir}}")
@task(returns=1, time_out=alya_timeout)
def simulation(name_sim, simulation_wdir, **kwargs):
    return
