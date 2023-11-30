import os
import numpy as np
import yaml

from PHASES.MODEL_TRAINING import trainingModel as train

def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases = data.get("phases")
        workflow_execution(execution_folder, phases.get("training"), data.get("outputs"), data.get("inputs"))
    return


def workflow_execution(execution_folder, training, outputs, inputs):
    x = np.load(inputs.get("x"))
    y = np.load(inputs.get("y"))
    results_folder = execution_folder + "/results/"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)
    res = train.training(x, y, training)
    train.write_file(results_folder, res, outputs=outputs)
    return


