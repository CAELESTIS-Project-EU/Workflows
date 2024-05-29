import os
from dislib.model_selection import GridSearchCV
import pandas as pd
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(X=COLLECTION_IN, Y=COLLECTION_IN)
def twinkle(X, Y, Kfold_divisions, training_params, kernel, results_folder, **kwargs):
    params = {}
    for key, value in training_params.items():
        params[key] = value
    estimate_Twinkle = kernel
    print("HERE")
    print(f"estimate_Twinkle: {estimate_Twinkle}")
    searcher = GridSearchCV(estimate_Twinkle, params, cv=Kfold_divisions)
    searcher.fit(X,Y)
    df = pd.DataFrame(searcher.cv_results_)
    file_out = os.path.join(results_folder, 'cv_results.csv')
    df.to_csv(file_out, index=False)
