import importlib
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(returns=1)
def training(training_type, **kwargs):
    module = importlib.import_module('PHASES.MODEL_TRAINING.' + training_type)
    return getattr(module, 'training')(**kwargs)
