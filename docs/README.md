# COMPSs Workflows

## Introduction

The COMPSs team has integrated CAELESTIS workflows into their library to manage the execution of various software and data analytics techniques while minimizing redundant code.

COMPSs Workflows function as templates that define abstract phases, which can be customized with different implementations. This allows engineers to evaluate individual processes or multiple processes together without having to develop a full workflow from scratch each time. Users can leverage existing workflows and phases or create new ones as needed.

### Cloning the repository and creating a new branch

```sh
$ git clone https://github.com/CAELESTIS-Project-EU/Workflows.git
$ cd Workflows
$ git checkout -b my_new_version
```

## Adding New Workflow Templates

To add a new workflow template, developers must create a new Python module within the `WORKFLOWS` folder of the GitHub repository. The process involves the following steps:

### Creating the workflow directory and files

```sh
$ cd WORKFLOWS/
$ mkdir <NEW_WORKFLOW_NAME>
$ cd <NEW_WORKFLOW_NAME>
$ touch __init__.py
$ touch my_new_workflow.py
```

### Implementing the workflow

Create a Python script file to implement the workflow template code. This script should adhere to the following structure:

- Import the `PHASES.utils` module to execute the phases defined in the workflow description (YAML file).
- Define the function that implements the workflow's behavior.
- The workflow function's interface must include:
  - `execution_folder`: Path to the directory created for running the workflow.
  - `data_folder`: Path where input data is stored when a relative path is defined.
  - `phases`: Description of the workflow's phases.
  - `inputs`: Key-value map of inputs.
  - `outputs`: Key-value map of outputs.
  - `parameters`: Key-value map storing the workflow's parameters.

```python
from PHASES.utils import phase
from pycompss.api.api import compss_wait_on

def execution(execution_folder, data_folder, phases, inputs, outputs, parameters):
    phase_output = phase.run(phases.get("phase_name"), inputs, outputs, parameters, data_folder, locals())
    phase_output = compss_wait_on(phase_output)
```

Workflows are implemented using the PyCOMPSs programming model, where computations are executed remotely and asynchronously to exploit the inherent parallelism of the workflow. To inspect the values of data generated in a phase, use the `compss_wait_on` method.

More information about developing PyCOMPSs workflows can be found [here](https://compss.readthedocs.io/en/stable/Sections/02_App_Development/02_Python.html).

## Adding New Phases

Adding new phases follows a similar process to adding a new workflow template:

### Creating the phase module

```sh
$ cd PHASES
$ mkdir <NEW_PHASE_NAME>
$ cd <NEW_PHASE_NAME>
$ touch __init__.py
$ touch my_new_phase.py
```

### Implementing the phase

Two main phase types are supported:

- **Single-task phases**: Involve a single computation.
- **Subworkflow phases**: Contain smaller algorithms that can execute multiple parallel computations.

#### Single-task phase example

```python
from pycompss.api.task import task
from pycompss.api.parameter import *

@task(path_A=DIRECTORY_IN, path_B=FILE_OUT, returns=2)
def my_phase_function(path_A, path_B, **kwargs):
    return a, b
```

#### Subworkflow phase example

```python
from pycompss.api.task import task
from pycompss.api.parameter import *

@task(input_file=FILE_IN, returns=1)
def process(input_file):
    return out

@task(accum=INOUT)
def merge(accum, new_data):
    accum.update(new_data)

def my_phase_function(files, **kwargs):
    accum = Accum(0)
    for file in files:
        out = process(file)
        merge(accum, out)
    return compss_wait_on(accum)
```

## Creating the workflow description

The examples folder contains descriptions of the workflows defined in both AutomationML and YAML formats. The AutomationML format is recommended for Industry 4.0 and is the format supported at HTP and HPC levels. The YAML format is easier to integrate with Python due to its direct mapping to Python data structures. YAML was used for the initial implementations of the HPC simulation service, maintaining support for this format in the HPC part; however, it is not supported at the HTP level. From the perspective of workflow execution descriptions, both formats contain equivalent information. YAML is more human-readable due to its lower verbosity, and therefore, the examples in this document are provided in YAML format.

### Workflow Description Example

A workflow description follows the YAML structure below and it contains the following sections, specified as key-value pairs.
- `workflow_type`: the template selected for the workflow, in the format `WORKFLOWS.<NEW_WORKFLOW_NAME>.<my_new_workflow>.<my_new_workflow_function>`.
- `phases`: the implementation selected for each workflow phase.
- `inputs` and `outputs`: external data movements, if required for execution.
- `parameters`: other parameters used in the workflow.
- `environment`: additional environment variables to be set during execution.

```yaml
workflow_type: WORKFLOWS.SENSITIVITY_ANALYSIS.workflow.execution
phases:
sampler:
…
prepare_data:
…
sim:
…
post_process:
…
sensitivity:
…
inputs:
…
outputs:
…
parameters:
-
problem:
- num_vars: 21
- variables-sampler:
- E11: {mean: 171420.0, cov: 1.39}
…
environment:
-
ALYA_PROCS: 112
```

### Phase specification 

The implementation of the phase is defined in the type field, in the format `PHASES.<NEW_PHASE_NAME>.<my_new_phase>.<my_new_phase_function>` while the `arguments` field contains extra parameters required for execution. The value of a phase argument can reference workflow parameters, input/output data paths, or internal workflow variables. In the followie following example, the problem argument in the sampler phase links to the problem parameter defined in the parameters section of theworkflow description. 

```yaml
workflow_type: WORKFLOWS.SENSITIVITY_ANALYSIS.workflow.execution 
phases: 
  sampler: 
    type: PHASES.SAMPLERS.morris.sampling 
    arguments: 
      - r: 20 
      - p: 16 
      - problem: ${parameters.problem} 
      ... 
```

### Input and output data transfers 

To describe the input and output data transfers required by the workflow, the path where data is stored in the computing site and the URL where data is stored on the storage server must be specified. Additionally, a flag can be set to overwrite existing files. An example of these descriptions is shown below: 

```yaml
…
inputs:
mesh:
- server: "ftp://nas.aimen.es/P_CAELESTIS_SHARE/input/meshes/OHT_Validation_D2"
- path: "meshes/OHT_Validation_D2"
outputs:
sesitivity_report:
- path: results.txt
- server: "ftp://nas.aimen.es/P_CAELESTIS_SHARE/outputs/test2J"
- overwrite: true
…
```

The full yaml file used for this example can be found [here](https://github.com/CAELESTIS-Project-EU/Workflows/blob/main/examples/yamls/SENSITIVITY/GSA_OHT_Validation_D2.yaml)

## Pushing the workflow

Once the developer has implemented the workflow, it can be pushed to the git repository with the following command.

```sh
~/Workflows/$ git pull origin my_new_version
```

The new workflow template can be tested by specifying the branch when submitting the workflow to the HPC service. After successful validation, it can be merged into the main branch by creating a pull request on GitHub.


## Executing and Testing

Workflows are executed by calling `/WORKFLOWS/api.py` passing the YAML file, an execution folder path, and a data folder path.

To run workflows on MareNostrum:

```sh
enqueue_compss \
--project_name=project_name \
--qos=gp_debug \
--pythonpath=/path/to/pythonpath/ \
/$INSTALL_FOLDER/WORKFLOWS/api.py \
/path/to/yaml_file.yaml /path/to/execution_folder /path/to/data_folder
```

### Example shell script

```sh
YAML=/path/to/yaml_file.yaml
EXEC_NAME=execution_name
NUM_NODES=2
EXEC_TIME=60
EXECUTION_FOLDER=/path/to/execution_folder/
QOS=gp_debug
PROJECT=project_name
INSTALL_FOLDER=/path/to/install_folder/
DATA_FOLDER=/path/to/data_folder/

module load hdf5
module load python/3.12.1
module load COMPSs/3.3.2

export PYTHONPATH=$INSTALL_FOLDER:$PYTHONPATH

cd $EXECUTION_FOLDER
enqueue_compss -d \
--project_name=$PROJECT \
--log_dir=$EXECUTION_FOLDER \
--scheduler=es.bsc.compss.scheduler.orderstrict.fifo.FifoTS \
--qos=$QOS \
--exec_time=$EXEC_TIME \
--pythonpath=$PYTHONPATH \
--num_nodes=$NUM_NODES \
$INSTALL_FOLDER/WORKFLOWS/api.py $YAML $EXECUTION_FOLDER $DATA_FOLDER
```
