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
    outputs = kwargs.get("outputs")
    alya_output_list = outputs.get("alya_output")
    # Initialize file_path to None
    file_path = None
    # Iterate over each dictionary in the list
    for item in alya_output_list:
        if "path" in item:
            file_path = item["path"]
            break  # Stop the loop once the path is found
    # Check if file_path was found
    if file_path is not None:
        # You can now use file_path for further processing
        file = str(file_path)
        y_file = output_folder + "/" + file
        module = importlib.import_module('PHASES.POSTSIMULATION.' + type)
        getattr(module, 'write_yFile')(y_file, y_param)
    return


