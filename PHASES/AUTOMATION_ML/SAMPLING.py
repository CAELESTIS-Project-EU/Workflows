import os
import pandas as pd
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(returns=2)
def run(path, **kwargs):
    csv_file_path = os.path.normpath(path)
    # Open the CSV file
    with open(csv_file_path, 'r') as file:
        df = pd.read_csv(csv_file_path)
        # List of columns to drop
        columns_to_drop = ['RUN_LEVEL', 'Filename', 'RUN_NAME']
        columns_exist = all(
            column in df.columns for column in columns_to_drop)  # Check if the columns exist before dropping
        if columns_exist:
            df = df.drop(columns=columns_to_drop)
        DoE_names = df.columns
    return df, DoE_names