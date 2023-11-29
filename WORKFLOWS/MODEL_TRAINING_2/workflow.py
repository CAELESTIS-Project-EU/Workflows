import numpy as np
import yaml
from PHASES.MODEL_TRAINING import trainingModel as train

def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases = data.get("phases")
        workflow_execution(phases.get("training"))
    return


def workflow_execution(training):
    x = np.array([[1.27979699e+00, 3.47209053e+01, 1.97452797e+03],
             [1.29823335e+00, 3.40782408e+01, 2.10593509e+03]])
    y = np.array([[20118.888],
             [20424.085]])

    results_folder="/home/bsc19/bsc19518/result_p/"
    res = train.training(x, y, training)
    train.write_file(results_folder, res)
    return


