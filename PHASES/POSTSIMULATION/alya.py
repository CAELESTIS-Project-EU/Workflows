import os
from pycompss.api.task import task
from pycompss.api.parameter import *
import yaml

@task(returns=1)
def collect_results(post_process_args):
    wdir=get_value(post_process_args, "simulation_wdir")
    nameSim = get_value(post_process_args, "nameSim")
    y = 0
    path = wdir + "/" + nameSim + "-output.sld.yaml"
    try:
        f = open(path)
        data = yaml.load(f, Loader=yaml.FullLoader)
        variables = data.get("variables")
        y = variables.get("FRXID")
    except Exception as e:
        print("NOT FINDING THE RESULT FILE OF ALYA")
        return 0
    return y

@task(y_param=COLLECTION_IN)
def write_yFile(write_file_args):
    alya_output = get_value(write_file_args, "alya_output")
    if alya_output is not None:
        result_folder = write_file_args.get("result_folder")
        y_elements = write_file_args.get("y")
        y_file = os.path.join(result_folder, alya_output)
        with open(y_file, 'w') as f3:
            f3.write("Y COLLECT: \n")
            i = 0
            for y in y_elements:
                s = str(y)
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
    for item in element:
        if param in item:
            problem_dict = item['problem']
            return problem_dict
    else:
        raise ValueError