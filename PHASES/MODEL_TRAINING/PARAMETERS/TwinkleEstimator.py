import os
import uuid
import numpy as np
from sklearn.base import BaseEstimator
from pycompss.api.parameter import *
from pycompss.api.task import task
from PHASES.MODEL_TRAINING.twinkle import twinkle_train_npoints, twinkle_train_mpoints, twinkle_score, twinkle_predict, post_twinkle
import dislib as ds

def gen_param(execution_folder, template, results_folder, var_results, score_weights, **kwargs):
    twinkle = TwinkleMyEstimator(execution_folder, template, results_folder, var_results, score_weights)
    return twinkle


class TwinkleMyEstimator(BaseEstimator):
    def __init__(self, execution_folder, template, results_folder, var_results, score_weights):
        self.mpoints = None
        self.npoints = None
        self.gtol = None
        self.ttol = None
        self.terms = None
        self.romFile = None
        self.template = template
        self.alsiter = None
        self.wflag = None
        self.romFile = None
        self.template_evalFile = None
        self.execution_folder = execution_folder
        self.results_folder= results_folder
        self.num_columns_y= len(var_results)
        self.name_folder=None
        self.var_results=var_results
        self.i=None
        self.score_weights= score_weights
        self.variable=None

    def __str__(self):
        return (f"mpoints: {self.mpoints}\n"
                f"npoints: {self.npoints}\n"
                f"gtol: {self.gtol}\n"
                f"ttol: {self.ttol}\n"
                f"terms: {self.terms}\n"
                f"romFile: {self.romFile}\n"
                f"template: {self.template}\n"
                f"alsiter: {self.alsiter}\n"
                f"wflag: {self.wflag}\n"
                f"template_evalFile: {self.template_evalFile}\n"
                f"execution_folder: {self.execution_folder}\n"
                f"results_folder: {self.results_folder}\n"
                f"num_columns_y: {self.num_columns_y}\n"
                f"name_folder: {self.name_folder}\n"
                f"var_results: {self.var_results}\n"
                f"i: {self.i}\n"
                f"variable: {self.variable}\n"
                f"score_weights: {self.score_weights}\n")


    def set_variable(self, variable):
        self.variable = variable
        return self

    def fit(self, X, Y):
        max_min_file_path = os.path.join(self.results_folder, "max_min_file.csv")
        max_min_data = np.loadtxt(max_min_file_path, delimiter=';', skiprows=1)
        n_inps = len(max_min_data[0]) - self.num_columns_y
        file_temp = os.path.join(self.execution_folder, "input" + self.template + ".csv")
        save_file_fit(X._blocks, max_min_data, Y._blocks, n_inps, self.i,  file_temp)
        if not self.mpoints and self.npoints:
            twinkle_train_npoints(file_temp, self.template, self.romFile, self.gtol, self.ttol, self.terms, self.alsiter,self.wflag, self.npoints, working_dir=self.execution_folder)
        elif self.mpoints and not self.npoints:
            twinkle_train_mpoints(file_temp, self.template, self.romFile, self.gtol, self.ttol, self.terms,
                                  self.alsiter, self.wflag, self.npoints, working_dir=self.execution_folder)
        else:
            raise ValueError("ERROR MPOINTS AND NPOINTS")
        return



    def set_varialbe(self, variable):
        self.varaible=variable
        return

    def set_params(self, **kwargs):
        name_folder=""
        if 'i' in kwargs:
            name_folder = "variable_"+str(kwargs.get("i"))+"__"

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                if key!="i":
                    name_folder+=str(key)+"_"+str(value)+"__"

        generated_uuid = uuid.uuid4()
        self.name_folder = name_folder+str(generated_uuid)
        out = os.path.join(self.execution_folder, "OUT")
        folder_random = os.path.join(out, self.name_folder)
        os.makedirs(folder_random, exist_ok=True)
        self.execution_folder = folder_random
        self.romFile = os.path.join(folder_random, "Results_" + self.template + ".txt")
        self.template_evalFile = self.template + "_eval"
        return self

    def score(self, X, Y, **kwargs):
        y_pred = self.predict(X)
        y_true = Y._blocks
        return twinkle_score(y_true, y_pred, self.execution_folder, self.score_weights)

    def predict(self, X, **kwargs):
        eval_file_tmp = os.path.join(self.execution_folder, "Eval_" + self.template + ".txt")
        out_file_tmp = os.path.join(self.execution_folder, "Prediction_" + self.template + "_eval.txt")
        save_file_predict(X._blocks, eval_file_tmp)
        twinkle_predict(self.romFile, eval_file_tmp, out_file_tmp, self.template_evalFile, working_dir=self.execution_folder)
        result = post_twinkle(out_file_tmp)
        return result



@task(x=COLLECTION_IN, data_set_file=FILE_OUT)
def save_file_predict(x, data_set_file):
    combined_data = np.block(x)
    print(f"shape X: {combined_data.shape}", flush=True)
    num_rows = combined_data.shape[0]
    zeros_array = np.zeros((num_rows, 1))
    combined= np.append(combined_data,zeros_array, axis=1)
    print(f"shape X_with_zeros: {combined.shape}", flush=True)
    print(f"save_file_predict shape eval_file_tmp: {combined.shape}", flush=True)
    np.savetxt(data_set_file, combined, delimiter=";")


@task(x=COLLECTION_IN, y=COLLECTION_IN, data_set_file=FILE_OUT)
def save_file_fit(x, max_min, y, n_inps, i, data_set_file):
    combined_y= np.concatenate((np.block(y), max_min[:, [n_inps+i]]), axis=0)
    print(f"combined_y: {combined_y.shape}", flush=True)
    combined_data = np.concatenate((np.block(x), max_min[:, :n_inps]), axis=0)
    print(f"combined_data: {combined_data.shape}", flush=True)
    combined= np.append(combined_data,combined_y, axis=1)
    print(f"save_file_fit input_csv: {combined.shape}", flush=True)
    np.savetxt(data_set_file, combined, delimiter=";")