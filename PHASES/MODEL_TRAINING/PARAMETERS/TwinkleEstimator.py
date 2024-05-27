import os
import uuid
import numpy as np
from sklearn.base import BaseEstimator
from pycompss.api.parameter import *
from pycompss.api.task import task
from PHASES.MODEL_TRAINING.twinkle import twinkle_train, twinkle_score, twinkle_predict, post_twinkle

@task(returns=1)
def gen_param(execution_folder, template, **kwargs):
    return TwinkleMyEstimator(execution_folder, template)

class TwinkleMyEstimator(BaseEstimator):
    def __init__(self, execution_folder, template, *, param=1):
        self.param = param
        self.mpoints = None
        self.npoints = None
        self.gtol = None
        self.ttol = None
        self.terms = None
        self.romFile = None
        self.template= template
        self.alsiter=None
        self.wflag=None
        self.romFile=None
        self.template_evalFile=None
        self.folder=execution_folder


    def __str__(self):
        return (f"param: {self.param}\n"
                f"mpoints: {self.mpoints}\n"
                f"npoints: {self.npoints}\n"
                f"gtol: {self.gtol}\n"
                f"ttol: {self.ttol}\n"
                f"terms: {self.terms}\n"
                f"romFile: {self.romFile}\n"
                f"template: {self.template}\n"
                f"alsiter: {self.alsiter}\n"
                f"wflag: {self.wflag}\n"
                f"template_evalFile: {self.template_evalFile}\n"
                f"folder: {self.folder}\n")


    def fit(self, X, Y):
        file_temp=os.path.join(self.folder,"input"+self.template+".csv")
        save_file(X._blocks, file_temp)
        twinkle_train(file_temp, self.template, self.romFile, self.gtol, self.ttol, self.terms, self.alsiter, self.wflag, working_dir=self.folder)
        return

    def set_params(self, **kwargs):
        # Iterate over the keyword arguments and set the attributes if they exist
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        generated_uuid = uuid.uuid4()
        out = os.path.join(self.folder, "OUT")
        folder_random = os.path.join(out, str(generated_uuid))
        os.makedirs(folder_random, exist_ok=True)
        self.folder= folder_random
        self.romFile = os.path.join(folder_random, "Results_" + self.template + ".txt")
        self.template_evalFile = self.template+"_eval"
        return self

    def score(self, X, Y, **kwargs):
        y_pred=self.predict(X)
        y_true=Y._blocks
        return twinkle_score(y_true, y_pred)

    def predict(self, X, **kwargs):
        eval_file_tmp=os.path.join(self.folder , "Eval_"+self.template + ".txt")
        out_file_tmp=os.path.join(self.folder , "Prediction_"+self.template + "_eval.txt")
        save_file(X._blocks, eval_file_tmp)
        twinkle_predict(self.romFile, eval_file_tmp, out_file_tmp, self.template_evalFile, working_dir=self.folder)
        result= post_twinkle(out_file_tmp)
        return result


@task(x=COLLECTION_IN, data_set_file=FILE_OUT)
def save_file(x, data_set_file):
    np.savetxt(data_set_file, np.block(x), delimiter=";")