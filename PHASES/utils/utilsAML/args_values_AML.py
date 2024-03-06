import os


def get_values(phase, inputs, outputs, parameters, data_folder, symbol_table):
    args_dict = None
    if phase:
        args_dict = get_arguments(phase, inputs, outputs, parameters, data_folder, symbol_table)
        return args_dict


def get_arguments(phase_args, inputs, outputs, parameters, data_folder, symbol_table):
    args = {}
    for key, value in phase_args.items():
        if starts_with_dollar(str(value)):
            search_params = remove_dollar_prefix(value)
            first_part, second_part = extract_parts(search_params)
            args.update(switch_values(first_part, second_part, inputs, outputs, parameters, data_folder, symbol_table))
        else:
            args.update({key: value})
    return args


def switch_values(first_part, second_part, inputs, outputs, parameters, data_folder, symbol_table):
    if first_part == "outputs":
        return get_outputs(second_part, outputs)
    elif first_part == "inputs":
        return get_inputs(second_part, inputs, data_folder)
    elif first_part == "parameters":
        return get_param(second_part, parameters)
    elif first_part == "variables":
        return add_entry(second_part, get_variable_value(second_part, symbol_table))
    else:
        raise ValueError(f"Unsupported first_part value: {first_part}")

def get_variable_value(variable_name, symbol_table):
    if variable_name in symbol_table:
        return symbol_table[variable_name]
    else:
        return f"Variable '{variable_name}' not found."

def extract_parts(input_string):
    # Splitting the string by periods
    parts = input_string.split('.')
    # Checking if there are at least two parts
    if len(parts) >= 2:
        # Extracting the first part
        first_part = parts[0]
        # Joining the remaining parts to form the second part
        second_part = ".".join(parts[1:])
        # Returning the two parts
        return first_part, second_part
    else:
        # If there are not enough parts, return None for both parts
        return None, None


def remove_dollar_prefix(s):
    return s[1:] if s.startswith("$") else s


def starts_with_dollar(input_string):
    return input_string.startswith("$")


def add_entry(key, value):
    new_entry = {key: value}
    return new_entry

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