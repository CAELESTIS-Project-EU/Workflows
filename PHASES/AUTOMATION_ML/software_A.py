"""from pycompss.api.task import task
from pycompss.api.parameter import *

@task(returns=1)"""
def run( **kwargs):
    s="Run Software A with "+ str(kwargs.get("execution_folder"))
    return s