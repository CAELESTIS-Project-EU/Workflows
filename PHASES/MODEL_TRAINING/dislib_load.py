import dislib as ds
import numpy as np
from pycompss.api.task import task
from pycompss.api.parameter import *


#@task(returns=2)
def load_twinkle(**kwargs):
    column = kwargs.get("column")
    blockSizeX = kwargs.get("blockSizeX")
    blockSizeY = kwargs.get("blockSizeY")
    input_file = kwargs.get("input_file")
    try:
        blockSizeX = eval(blockSizeX)
        blockSizeY = eval(blockSizeY)
    except Exception as e:
        raise ValueError(f"Error in evaluating blockSizeX or blockSizeY: {str(e)}")

    if column is None or blockSizeX is None or blockSizeY is None or input_file is None:
        raise ValueError("Required parameters are missing")
    else:
        X = ds.load_txt_file(input_file, blockSizeX, delimiter=";")[:, :column]
        Y = ds.load_txt_file(input_file, blockSizeY, delimiter=";")[:, [column]]
        return X, Y


@task(returns=1)
def load(**kwargs):
    inputFileX = kwargs.get("inputFileX")
    inputFileY = kwargs.get("inputFileY")
    if inputFileX is None or inputFileY is None:
        return get_from_numpy(kwargs.get("inputFileX"), kwargs.get("inputFileY"))


def get_from_numpy(inputFileX, inputFileY):
    X = np.load(inputFileX)
    Y = np.load(inputFileY)
    X = ds.array(X, block_size=X.shape)
    Y = Y[:, np.newaxis]
    Y = ds.array(Y, block_size=Y.shape)
    return X, Y
