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


def twinkle(X, Y, Kfold_divisions, training_params, kernel, results_folder, var_results, **kwargs):
    estimate_Twinkle = kernel
    searchers=[]
    #searcher en una lista y after to_csv para cada uno sercher en otro loop
    for i in range (len(var_results)):
        searcher = GridSearchCV(estimate_Twinkle, training_params, cv=Kfold_divisions)
        searcher.fit(X,[Y[:,i]])
        searchers.append(searcher)


    for searcher, i in enumerate(searchers):
        df = pd.DataFrame(searcher.cv_results_)
        #dentro de result forlder crear una carpeta che se llama con el nombre y valores de los parametros del twinkle estimator  por execution folder and result folder
        folder=os.path.join(results_folder, var_results[i])
        if not os.path.isdir(folder):
            os.makedirs(folder)
        file_out = os.path.join(folder, "cv_results.csv")
        best_estimator_file=searcher.best_estimator.romFile
        compss_wait_on_file(best_estimator_file)
        shutil.copyfile(best_estimator_file, os.path.join(folder, "rom_file.txt"))
        #searcher.best_estimator.folder_name
        df.to_csv(file_out, index=False)


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
        data = pd.read_csv(result_file, skiprows=1, delim_whitespace=True)
    except FileNotFoundError:
        raise Exception(f"The file {result_file} does not exist.")
    return data.to_numpy()


@task(y_blocks=COLLECTION_IN, returns=1)
def twinkle_score(y_blocks, y_pred):
    y_true=np.block(y_blocks)
    print(f"shape y_true: {y_true.shape}", flush=True)
    print(f"shape y_pred: {y_pred.shape}", flush=True)
    if y_true.shape!=y_pred.shape:
        return 0
    return r2_score(y_true, y_pred)