from pycompss.api.api import compss_wait_on
import numpy as np
from pycompss.api.task import task
from pycompss.api.parameter import *
from PHASES.utils import args_values, phase
import os



def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    phase.run(phases.get("train"), inputs, outputs, parameters, data_folder, locals())
    phase.run(phases.get("predict"), inputs, outputs, parameters, data_folder, locals())
    return


@task(elements=COLLECTION_IN)
def write_file(output_folder, elements, nameFile, **kwargs):
    model_file= os.path.join(output_folder, nameFile)
    write(model_file, elements)


def write(file, element):
    with open(file, 'wb') as f3:
        np.save(f3, element)
        f3.close()
    return