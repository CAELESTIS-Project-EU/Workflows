from pycompss.api.mpi import mpi
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.on_failure import on_failure
import os

alya_procs=int(os.environ.get("ALYA_PROCS", "2"))
alya_ppn=int(os.environ.get("ALYA_PPN", "2"))
if alya_procs < alya_ppn:
    alya_ppn=alya_procs

@on_failure(management='IGNORE')
@mpi(runner="mpirun", binary="$ALYA_BIN", args="{{case_name}}", processes=alya_procs, processes_per_node=alya_ppn, working_dir="{{simulation_wdir}}")
@task(returns=1, time_out=3600)
def simulation(case_name, simulation_wdir, **kwargs):
    return


def run_permeability(case_name, simulation_wdir, cases_permeability, **kwargs):
    results=[]
    for case in cases_permeability:
        simulation_wdir_case = os.path.join(simulation_wdir, case)
        results.append(simulation(case_name, simulation_wdir_case, **kwargs))
    return results

def run_rve(case, simulation_wdir, listloads, **kwargs):
    results=[]
    for load in listloads:
        name = case + "-"+str(load)
        simulation_wdir_case = os.path.join(simulation_wdir, name)
        results.append(simulation(name, simulation_wdir_case, **kwargs))
    return results