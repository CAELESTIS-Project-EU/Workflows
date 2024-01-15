import os
from pycompss.api.task import task
from pycompss.api.parameter import *
import yaml


@task(returns=1)
def collect_results(**kwargs):
    post_process_args = kwargs.get("args")
    wdir = get_value(post_process_args, "simulation_wdir")
    name_sim = get_value(post_process_args, "name_sim")
    y = 0
    path = wdir + "/" + name_sim + "-output.sld.yaml"
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
def write_results(y, alya_output, results_folder, **kwargs):
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
    return


def get_value(element, param):
    if param in element:
        return element[param]
    else:
        raise ValueError(f"The key '{param}' was not found in the dictionary.")
