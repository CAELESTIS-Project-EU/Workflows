import importlib
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(y_param=COLLECTION_IN, returns=1)
def training(x, y, training, **kwargs):
    training_type=training.get("type")
    module = importlib.import_module('PHASES.MODEL_TRAINING.' + training_type)
    return getattr(module, 'training')(x, y, training, **kwargs)

@task(y_param=COLLECTION_IN)
def write_file(output_folder, y_param, sample_set, res, **kwargs):
    outputs = kwargs.get("outputs")
    model_output = outputs.get("model-output")
    # Initialize file_path to None
    file_path = None
    # Iterate over each dictionary in the list
    for item in model_output:
        if "path" in item:
            file_path = item["path"]
            break  # Stop the loop once the path is found
    # Check if file_path was found
    if file_path is not None:
        # You can now use file_path for further processing
        file = str(file_path)
        model_file = output_folder + "/" + file
        write_File(model_file, y_param, sample_set, res)

def write_File(file, y, sample_set, res):
    with open(file, 'w') as f3:
        f3.write("Y MODEL RES: \n")
        f3.write(str(res))
        f3.close()
    return