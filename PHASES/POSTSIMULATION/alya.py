import os

import numpy as np
from pycompss.api.task import task
from pycompss.api.parameter import *
import yaml


@task(returns=1)
def collect_results(simulation_wdir, name_sim, out, **kwargs):
    y = 0
    path=os.path.join(simulation_wdir, name_sim + "-output.sld.yaml")
    #path = simulation_wdir + "/" + name_sim + "-output.sld.yaml"
    try:
        f = open(path)
        data = yaml.load(f, Loader=yaml.FullLoader)
        variables = data.get("variables")
        y = variables.get("FRXID")
    except Exception as e:
        print("NOT FINDING THE RESULT FILE OF ALYA")
        return 0
    return y


@task(y=COLLECTION_IN, returns=1)
def write_results(y, alya_output, results_folder, sample_set, **kwargs):
    """write_file_args = kwargs.get("args")
    alya_output = get_value(write_file_args, "alya_output")"""
    if alya_output is not None:
        """results_folder = get_value(write_file_args, "results_folder")
        y_elements = get_value(write_file_args, "y")"""
        y_file = os.path.join(results_folder, alya_output)
        with open(y_file, 'w') as f3:
            f3.write("Y COLLECT: \n")
            i = 0
            for y_element in y:
                s = str(y_element)
                """s=str(x)+"["
                for j in range(probDef.get("num_vars")):
                    s=s+(probDef.get("names")[j]+"="+str(param_values[i][j])+"; ")
                s=s+"]\n"""
                s = s + "\n"
                i += 1
                f3.write(s)
            f3.write("Y size: " + str(i))
            f3.close()
        write_file(results_folder, sample_set, "dataSet_matrix.npy")
        write_file(results_folder, y, "result_array.npy")
    return




def write_file(output_folder, elements, nameFile, **kwargs):
    model_file= os.path.join(output_folder, nameFile)
    write(model_file, elements)
    return 


def write(file, element):
    with open(file, 'wb') as f3:
        np.save(f3, element)
        f3.close()
    return

def get_value(element, param):
    if param in element:
        return element[param]
    else:
        raise ValueError(f"The key '{param}' was not found in the dictionary.")
