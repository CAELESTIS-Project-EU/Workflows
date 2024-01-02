import importlib
import os.path

from pycompss.api.task import task
from pycompss.api.parameter import *


@task(returns=1)
def collect(type, wdir, nameSim, out):
    module = importlib.import_module('PHASES.POSTSIMULATION.' + type)
    y = getattr(module, 'collect_results')(wdir, nameSim)
    return y


@task(y_param=COLLECTION_IN)
def write_file(type, output_folder, y_param, **kwargs):
    outputs = kwargs.get("outputs")
    alya_output = outputs.get("alya_output")
    # Check if file_path was found
    if alya_output is not None:
        y_file = os.path.join(output_folder, alya_output)
        module = importlib.import_module('PHASES.POSTSIMULATION.' + type)
        getattr(module, 'write_yFile')(y_file, y_param)
    return
