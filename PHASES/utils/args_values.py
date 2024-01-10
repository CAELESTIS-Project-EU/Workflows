import os


def get_param(value_in, parameters_yaml):
    param = extract_value(parameters_yaml, value_in)
    parameters = {value_in: param}
    return parameters


def get_inputs(value_in, input_yaml, data_folder):
    input_folder = extract_value_files(input_yaml, value_in)
    input_folder = os.path.join(data_folder, input_folder) if input_folder else None
    inputs = {value_in: input_folder}
    return inputs


def get_outputs(value_in, outputs_yaml):
    outputs_folder = extract_value_files(outputs_yaml, value_in)
    outputs= {value_in:outputs_folder}
    return outputs


def extract_value_files(yaml, name):
    value = yaml.get(name, [])
    value_folder = ""
    for item in value:
        if isinstance(item, dict) and 'path' in item:
            value_folder = item['path']
            break
    return value_folder

def extract_value(yaml, name):
    value = yaml.get(name, [])
    return value