import os
import uuid
import numpy as np
from sklearn.base import BaseEstimator
from pycompss.api.parameter import *
from pycompss.api.task import task
from PHASES.MODEL_TRAINING.twinkle import twinkle_train, twinkle_score, twinkle_predict, post_twinkle
import dislib as ds

def gen_param(execution_folder, template, results_folder, num_columns_y, **kwargs):
    twinkle = TwinkleMyEstimator(execution_folder, template, results_folder, num_columns_y)
    return twinkle


class TwinkleMyEstimator(BaseEstimator):
    def __init__(self, execution_folder, template, results_folder, num_columns_y, *, param=1):
        self.param = param
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
        self.num_columns_y= num_columns_y

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
                f"execution_folder: {self.execution_folder}\n")

    def fit(self, X, Y):

        max_min_file_path = os.path.join(self.results_folder, 'max_min_file.csv')
        max_min_data = np.loadtxt(max_min_file_path, delimiter=';', skiprows=1)
        n_inps = len(max_min_data[0]) - self.num_columns_y
        #Y = max_min_data[:, -self.num_columns_y:]
        combined_data = np.concatenate((X.collect(), max_min_data[:, :n_inps]), axis=0)
        X_combined = ds.array(combined_data, block_size=combined_data.shape)

        file_temp = os.path.join(self.execution_folder, "input" + self.template + ".csv")
        save_file(X_combined._blocks, file_temp)
        twinkle_train(file_temp, self.template, self.romFile, self.gtol, self.ttol, self.terms, self.alsiter,
                      self.wflag, working_dir=self.execution_folder)
        return

    def set_params(self, **kwargs):
        # Iterate over the keyword arguments and set the attributes if they exist
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        generated_uuid = uuid.uuid4()
        out = os.path.join(self.execution_folder, "OUT")
        folder_random = os.path.join(out, str(generated_uuid))
        os.makedirs(folder_random, exist_ok=True)
        self.execution_folder = folder_random
        self.romFile = os.path.join(folder_random, "Results_" + self.template + ".txt")
        self.template_evalFile = self.template + "_eval"
        return self

    def score(self, X, Y, **kwargs):
        y_pred = self.predict(X.collect())

        max_min_file_path = os.path.join(self.results_folder, 'max_min_file.csv')
        max_min_data = np.loadtxt(max_min_file_path, delimiter=';', skiprows=1)
        combined_data = np.concatenate((Y.collect(), max_min_data[:, -self.num_columns_y:]), axis=0)
        Y_combined = ds.array(combined_data, block_size=combined_data.shape)

        y_true = Y_combined._blocks
        return twinkle_score(y_true, y_pred)

    def predict(self, X, **kwargs):
        eval_file_tmp = os.path.join(self.execution_folder, "Eval_" + self.template + ".txt")
        out_file_tmp = os.path.join(self.execution_folder, "Prediction_" + self.template + "_eval.txt")

        max_min_file_path = os.path.join(self.results_folder, 'max_min_file.csv')
        max_min_data = np.loadtxt(max_min_file_path, delimiter=';', skiprows=1)
        n_inps = len(max_min_data[0]) - self.num_columns_y
        combined_data = np.concatenate((X, max_min_data[:, :n_inps]), axis=0)
        X_combined = ds.array(combined_data, block_size=combined_data.shape)

        save_file(X_combined._blocks, eval_file_tmp)
        twinkle_predict(self.romFile, eval_file_tmp, out_file_tmp, self.template_evalFile, working_dir=self.execution_folder)
        result = post_twinkle(out_file_tmp)
        return result


@task(x=COLLECTION_IN, data_set_file=FILE_OUT)
def save_file(x, data_set_file):
    np.savetxt(data_set_file, np.block(x), delimiter=";")
