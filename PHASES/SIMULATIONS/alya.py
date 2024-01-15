from pycompss.api.mpi import mpi
from pycompss.api.task import task
from pycompss.api.parameter import *


@mpi(runner="mpirun", binary="$ALYA_BIN", args="{{name_sim}}", processes="$ALYA_PROCS", processes_per_node="$ALYA_PPN", working_dir="{{simulation_wdir}}")
@task(returns=1, time_out=3600)
def run_simulation(name_sim, simulation_wdir, **kwargs):
    return


def simulation(**kwargs):
    sim_args = kwargs.get("args")
    name_sim = get_value(sim_args, "name_sim")
    simulation_wdir = get_value(sim_args, "simulation_wdir")
    run_simulation(name_sim, simulation_wdir, **kwargs)
    return


def get_value(element, param):
    for item in element:
        if param in item:
            return item[param]
    else:
        raise ValueError(f"The key '{param}' was not found in the dictionary.")
