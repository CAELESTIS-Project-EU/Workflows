import dislib as ds
from pycompss.api.task import task
from pycompss.api.parameter import *

@task(returns=1)
def load(inputFile):
    X = ds.load_txt_file(inputFile, (300, 2), delimiter=";")[:, :4]
    Y = ds.load_txt_file(inputFile, (300, 1), delimiter=";")[:, [4]]

    x = ds.array(x, block_size=x.shape)
    y = np.array(y)
    y = y[:, np.newaxis]
    y = ds.array(y, block_size=y.shape)