import numpy as np
import yaml
from sklearn.datasets import make_regression

from PHASES.MODEL_TRAINING import trainingModel as train

def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases = data.get("phases")
        workflow_execution(phases.get("training"))
    return


def workflow_execution(training):
    """x = np.array([[1.27979699e+00, 3.47209053e+01, 1.97452797e+03],[1.29823335e+00, 3.40782408e+01, 2.10593509e+03], [1.31479699e+00, 3.76549053e+01, 1.97852797e+03],[1.32979699e+00, 3.50209053e+01, 1.91452797e+03],[1.43979699e+00, 3.52209053e+01, 1.92452797e+03],[1.33979699e+00, 3.42209053e+01, 1.95452797e+03],[1.33979699e+00, 3.46209053e+01, 1.98452797e+03],[1.27979699e+00, 3.47209053e+01, 1.97452797e+03],[1.27979699e+00, 3.47209053e+01, 1.97452797e+03],[1.27979699e+00, 3.47209053e+01, 1.97452797e+03],[1.27979699e+00, 3.47209053e+01, 1.97452797e+03]])
    y = [20118.888, 20424.085, 20158.085, 20256.085, 20578.085, 20578.085, 20354.085, 20424.085, 20424.085, 20424.085, 20424.085]"""
    x, y = make_regression(n_samples=5, n_features=2, noise=1, random_state=42)
    results_folder="/home/bsc19/bsc19518/result_p/"
    res = train.training(x, y, training)
    train.write_file(results_folder, res)
    return


