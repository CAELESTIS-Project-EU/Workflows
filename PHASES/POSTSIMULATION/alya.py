from pycompss.api.task import task
from pycompss.api.parameter import *
import yaml


def collect_results(wdir, nameSim):
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


def write_yFile(file, y_elements):
    with open(file, 'w') as f3:
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
