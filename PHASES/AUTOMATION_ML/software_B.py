"""from pycompss.api.task import task
from pycompss.api.parameter import *


@task(returns=1)"""
def run(**kwargs):
    print("Run Software B with ", kwargs.values())
    return