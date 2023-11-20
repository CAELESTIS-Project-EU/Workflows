import importlib
from pycompss.api.task import task
from pycompss.api.parameter import *

@task(returns=1)
def collect(type, wdir, nameSim, out):
    module = importlib.import_module('PHASES.POSTSIMULATION.' + type)
    y=getattr(module, 'collect_results')(wdir, nameSim)
    return y

@task(y_param=COLLECTION_IN)
def write_file(type, output_folder, y_param, **kwargs):
    file=str(kwargs.get("outputs").get("alya-output"))
    y_file=output_folder+"/"+file
    module = importlib.import_module('PHASES.POSTSIMULATION.' + type)
    getattr(module, 'write_yFile')(y_file, y_param)
    return

