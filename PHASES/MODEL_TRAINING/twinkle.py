import copy
import os
from dislib.model_selection import GridSearchCV
import pandas as pd
from sklearn.metrics import r2_score
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.container import container
from pycompss.api.binary import binary
from pycompss.api.api import compss_wait_on_file
import numpy as np
import shutil
from pycompss.api.constraint import constraint
from sklearn import clone
from PHASES.MODEL_TRAINING.ERRORS.ROM_VerificationFit import data_analysis

twinkle_cu=int(os.environ.get("TWINKLE_CU", "2"))



def twinkle(X, Y, Kfold_divisions, training_params, kernel, results_folder, var_results, **kwargs):
    searchers=[]
    training_params=preprocess_training_params(training_params)
    for i in range (len(var_results)):
        training_params["i"]=[i]
        kernel.set_variable(var_results[i])
        searcher = GridSearchCV(kernel, training_params, cv=Kfold_divisions)
        searcher.fit(X,Y[:,[i]])
        searchers.append(searcher)


    for i, searcher in enumerate(searchers):
        df = pd.DataFrame(searcher.cv_results_)
        folder=os.path.join(results_folder, "Result_Case_"+var_results[i])
        if not os.path.isdir(folder):
            os.makedirs(folder)
        file_out = os.path.join(folder, "cv_results.csv")
        best_estimator_file=searcher.best_estimator_.romFile
        compss_wait_on_file(best_estimator_file)
        shutil.copyfile(best_estimator_file, os.path.join(folder, "rom_file.txt"))
        df.to_csv(file_out, index=False)


def preprocess_training_params(params):
    # Check the value of Adapted_Discretization
    adapted_discretization = params.get("Adapted_Discretization")

    if adapted_discretization in ['n', 'N']:
        # Remove Adapted_Discretization and npoints
        params.pop("Adapted_Discretization", None)
        params.pop("mpoints", None)
    elif adapted_discretization in ['Y', 'y']:
        # Remove Adapted_Discretization and mpoints
        params.pop("Adapted_Discretization", None)
        params.pop("npoints", None)

    return params

@constraint(computing_units=twinkle_cu)
@container(engine="SINGULARITY", options="-e", image="/home/bsc/bsc019518/MN4/bsc19518/Permeability/testPerm/Twinkle_DisLib/twinkle.sif")
@binary(binary="/Twinkle/runTwinkle", args="-file {{inputFile}} -out {{template_outFile}} -npoints {{npoints}} -gtol {{gtol}} -ttol {{ttol}} -terms {{terms}} -alsiter {{alsiter}} -wflag {{wflag}}", working_dir="{{working_dir}}")
@task(inputFile=FILE_IN, romFile=FILE_OUT)
def twinkle_train_npoints(inputFile, template_outFile, romFile, gtol, ttol, terms, alsiter, wflag, npoints, working_dir, **kwargs):
    pass


@constraint(computing_units=twinkle_cu)
@container(engine="SINGULARITY", options="-e", image="/home/bsc/bsc019518/MN4/bsc19518/Permeability/testPerm/Twinkle_DisLib/twinkle.sif")
@binary(binary="/Twinkle/runTwinkle", args="-file {{inputFile}} -out {{template_outFile}} -mpoints {{mpoints}} -gtol {{gtol}} -ttol {{ttol}} -terms {{terms}} -alsiter {{alsiter}} -wflag {{wflag}}", working_dir="{{working_dir}}")
@task(inputFile=FILE_IN, romFile=FILE_OUT)
def twinkle_train_mpoints(inputFile, template_outFile, romFile, gtol, ttol, terms, alsiter, wflag, npoints, working_dir, **kwargs):
    pass


@constraint(computing_units=twinkle_cu)
@container(engine="SINGULARITY", options="-e", image="/home/bsc/bsc019518/MN4/bsc19518/Permeability/testPerm/Twinkle_DisLib/twinkle.sif")
@binary(binary="/Twinkle/runTwinkle", args="-rom {{romFile}} -eval {{evalFile}} -out {{template_outFile}}", working_dir="{{working_dir}}")
@task(romFile=FILE_IN, evalFile=FILE_IN, outFile=FILE_OUT)
def twinkle_predict(romFile, evalFile, outFile, template_outFile, working_dir, **kwargs):
    pass


@constraint(computing_units=twinkle_cu)
@task(result_file=FILE_IN, returns=1)
def post_twinkle(result_file):
    try:
        data = pd.read_csv(result_file, skiprows=1, delim_whitespace=True, names=['prediction'])
    except FileNotFoundError:
        raise Exception(f"The file {result_file} does not exist.")
    return  data.to_numpy()


@constraint(computing_units=twinkle_cu)
@task(y_blocks=COLLECTION_IN, returns=1)
def twinkle_score(y_blocks, y_pred, execution_folder, score_weights):
    y_true=np.block(y_blocks)
    print(f"shape y_true: {y_true.shape}", flush=True)
    print(f"shape y_pred: {y_pred.shape}", flush=True)
    if y_true.shape!=y_pred.shape:
        print(f"DIFFERENT SHAPE  y_true:{y_true.shape}  y_pred: {y_pred.shape}")
        return 0
    report= data_analysis(y_pred, y_true, execution_folder)
    print(f"report: {report}")

    error=report['Mean_absolute_error'] * score_weights['Wmae'] +report['Mean10%ofMax_absolute_error'] * score_weights['W10mae']
    return error