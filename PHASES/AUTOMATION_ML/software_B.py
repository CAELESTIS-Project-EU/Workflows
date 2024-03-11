"""from pycompss.api.task import task
from pycompss.api.parameter import *


@task(returns=1)"""
def run(**kwargs):
    s="Run Software B with " + kwargs.get("B_description")
    print(s)
    return s