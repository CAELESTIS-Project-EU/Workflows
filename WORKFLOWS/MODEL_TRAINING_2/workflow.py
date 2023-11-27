import yaml
from PHASES.MODEL_TRAINING import trainingModel as train

def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        phases = data.get("phases")
        workflow_execution(phases.get("training"))
    return


def workflow_execution(training):
    train.training(training)
    return


