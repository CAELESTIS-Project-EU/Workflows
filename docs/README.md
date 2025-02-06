# COMPSs Workflows

## Introduction

The COMPSs team has integrated CAELESTIS workflows into their library to manage the execution of various software and data analytics techniques while minimizing redundant code.

COMPSs Workflows function as templates that define abstract phases, which can be customized with different implementations. This allows engineers to evaluate individual processes or multiple processes together without having to develop a full workflow from scratch each time. Users can leverage existing workflows and phases or create new ones as needed.

## Adding New Workflow Templates

To add a new workflow template, developers must create a new Python module within the `WORKFLOWS` folder of the GitHub repository. The process involves the following steps:

### Cloning the repository and creating a new Branch

```sh
$ git clone https://github.com/CAELESTIS-Project-EU/Workflows.git
$ cd Workflows
$ git checkout -b my_new_version
```

### Creating the workflow directory and files

```sh
$ cd WORKFLOWS/
$ mkdir <NEW_WORKFLOW_NAME>
$ cd <NEW_WORKFLOW_NAME>
$ touch __init__.py
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

### Creating the workflow description

The `phase.run` function executes a phase by retrieving its arguments from the YAML workflow description.

```yaml
phases:
  prepare_data:
    type: PHASES.BEFORESIMULATION.alya.prepare_data
    arguments:
      - mesh: $inputs.mesh
      - template_sld: $inputs.template_sld
      - problem: $parameters.problem
      - simulation_wdir: $variables.simulation_wdir
```

### Pushing the workflow

```sh
$ git pull origin my_new_version
```

The new workflow template can be tested by specifying the branch when submitting the workflow to the HPC service. After successful validation, it can be merged into the main branch by creating a pull request on GitHub.

## Adding New Phases

Adding new phases follows a similar process to adding a new workflow template:

### Cloning and branching

```sh
$ git clone https://github.com/CAELESTIS-Project-EU/Workflows.git
$ cd Workflows
$ git checkout -b my_new_version
```

### Creating the phase module

```sh
$ cd PHASES
$ mkdir <NEW_PHASE_NAME>
$ cd <NEW_PHASE_NAME>
$ touch __init__.py
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

More details can be found [here](https://compss.readthedocs.io/en/stable/Sections/02_App_Development/02_Python.html).

#### Defining the phase in the workflow description

```yaml
phases:
  <phase_name>:
    type: PHASES.<NEW_PHASE_NAME>.<my_new_phase>.<my_phase_function>
    arguments:
      - path_A: ...
      - path_B: ...
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

### Pushing the phase

```sh
$ git pull origin my_new_version
```

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
