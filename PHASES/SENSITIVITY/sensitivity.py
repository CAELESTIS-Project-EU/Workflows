from pycompss.api.task import task
from pycompss.api.parameter import *
import importlib

@task(y=COLLECTION_IN, param_values=COLLECTION_IN)
def analysis(problem, y, output_folder, param_values, **kwargs):
    outputs = kwargs.get("outputs")
    sesitivity_report = outputs.get("sesitivity_report")
    # Initialize file_path to None
    file_path = None
    # Iterate over each dictionary in the list
    for item in sesitivity_report:
        if "path" in item:
            file_path = item["path"]
            break  # Stop the loop once the path is found
    # Check if file_path was found
    if file_path is not None:
        file = str(file_path)
        output_file= output_folder+"/"+file
        type= kwargs.get("parameters").get("name")
        paramSampling= kwargs.get("paramSampling")
        args=[problem, y, param_values, output_file]
        module = importlib.import_module('PHASES.SENSITIVITY.' + type)
        res= getattr(module, type)(problem, y, param_values, output_file, outputs=(kwargs.get("parameters").get("outputs")), paramSampling=paramSampling)
        write_outputFile(output_file, res, kwargs.get("parameters").get("outputs"))
    
def write_outputFile(file, Si, outputs):
    with open(file, 'w') as f2:
        f2.write("OUTPUTS \n")
        for output in outputs:
            result = str(output) + ": "+str(Si.get(output))+"\n"
            f2.write(result)
        f2.close()
    return

def write_yFile(file, y, param_values, probDef):
    with open(file, 'w') as f3:
        f3.write("Y COLLECT: \n")
        i=0
        for x in y:
            s=str(x)+"["
            for j in range(probDef.get("num_vars")):
                s=s+(probDef.get("names")[j]+"="+str(param_values[i][j])+"; ")
            s=s+"]\n"
            i+=1
            f3.write(s)
        f3.write("Y size: "+str(i))
        f3.close()
    return

@task(returns=1)
def generate_path(type, output_folder, output, out5):
    module = importlib.import_module('PHASES.SENSITIVITY.' + type)
    return getattr(module, "generate_plot")(output_folder, output)