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
    x_path="/gpfs/scratch/bsc19/bsc19518/results/execution_12eaf6a0-143f-4709-b9cc-9811264a5100/execution/results/xfile.npy"
    y_path="/gpfs/scratch/bsc19/bsc19518/results/execution_12eaf6a0-143f-4709-b9cc-9811264a5100/execution/results/y.npy"
    results_folder="/gpfs/scratch/bsc19/bsc19518/results/execution_12eaf6a0-143f-4709-b9cc-9811264a5100/execution/results/"
    x=np.load(x_path)
    y = np.load(y_path)
    res = train.training(x, y, training)
    train.write_file(results_folder, res)
    return


