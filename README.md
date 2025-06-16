# CAELESTIS HPC WORKFLOWS

This repository stores the workflow templates and phases implementations use in the CAELESTIS Project. It is organized as follows:

- WORKFLOWS: This folder stores the workflow templates implemented for different analysis used in the CAELESTIS Project. This workflow templates have generic steps that can be customized with the AutomationML or YAML workflow descriptions.
- PHASES: This folder contains the different implementations of the workflow generic steps. This implementations are Python modules with functions that implement different sampling methods, simulations, post-processing and ML algorithms that can be used in the workflow templates.
- Examples: This folder contains different workflow description examples used in CAELESTIS either in YAML or AutomationML. This workflow description defines the workflow template and phases to execute together with the description of the input dataset and the expected results. 

## Workflow execution
To execute the workflows users has to use the CAELESTIS simulation service. Source code and instructions about how to deploy this service can be found [here](https://github.com/CAELESTIS-Project-EU). Documentation of how to run the workflows in the HPC site using the service can be found [here](https://caelestis-project-eu-simulations-service.readthedocs.io/en/latest/).

## Acknowledgements
This work has been developed in the CAELESTIS project. This project has received funding from the European Union’s HORIZON research and innovation program under grant agreement nº 101056886
