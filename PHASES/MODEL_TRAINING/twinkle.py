from dislib.model_selection import GridSearchCV
import dislib as ds
import pandas as pd
from sklearn.metrics import r2_score
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.container import container
from pycompss.api.binary import binary
from PHASES.MODEL_TRAINING.PARAMETERS.TwinkleEstimator import TwinkleMyEstimator


def twinkle(inputFile, Kfold_divisions, training_params, kernel, **kwargs):
    params = {}

    for key, value in training_params.items():
        params[key] = value
    print("PARAMS ENTER:", str(params))
    estimate_Twinkle = kernel
    X = ds.load_txt_file(inputFile, (300,2), delimiter=";")[:,:4]
    Y = ds.load_txt_file(inputFile, (300,1), delimiter=";")[:,[4]]
    searcher = GridSearchCV(estimate_Twinkle, params, cv=Kfold_divisions)
    searcher.fit(X,Y)
    #searcher.score(X)
    print("RESULT")
    #print(pd.DataFrame(searcher.cv_results_))
    return

@container(engine="SINGULARITY", options="-e", image="/home/bsc/bsc019518/MN4/bsc19518/Permeability/testPerm/Twinkle_DisLib/twinkle.sif")
@binary(binary="/Twinkle/runTwinkle", args="-file {{inputFile}} -out {{template_outFile}} -gtol {{gtol}} -ttol {{ttol}} -terms {{terms}} -alsiter {{alsiter}} -wflag {{wflag}}", working_dir="{{working_dir}}")
@task(inputFile=FILE_IN, romFile=FILE_OUT)
def twinkle_train(inputFile, template_outFile, romFile, gtol, ttol, terms, alsiter, wflag, working_dir, **kwargs):
    pass




@container(engine="SINGULARITY", options="-e", image="/home/bsc/bsc019518/MN4/bsc19518/Permeability/testPerm/Twinkle_DisLib/twinkle.sif")
@binary(binary="/Twinkle/runTwinkle", args="-rom {{romFile}} -eval {{evalFile}} -out {{template_outFile}}", working_dir="{{working_dir}}")
@task(romFile=FILE_IN, evalFile=FILE_IN, outFile=FILE_OUT)
def twinkle_predict(romFile, evalFile, outFile, template_outFile, working_dir, **kwargs):
    pass


@task(result_file=FILE_IN, returns=1)
def post_twinkle(result_file):
    try:
        data = pd.read_csv(result_file, skiprows=1, delim_whitespace=True, names=['data', 'prediction'])
    except FileNotFoundError:
        raise Exception(f"The file {result_file} does not exist.")
    return data['prediction'].to_numpy()


@task(returns=1)
def twinkle_score(y_true, y_pred):
    return r2_score(y_true, y_pred)
