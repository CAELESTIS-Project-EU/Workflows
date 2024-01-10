import yaml
import sys
import importlib


def workflow(path, execution_folder, data_folder):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        workflow_type=data.get("workflow_type")
        parameters=data.get("parameters")
        module_call, function_call = split_string_at_last_dot(workflow_type)
        module = importlib.import_module(module_call)
        getattr(module, function_call)(data, execution_folder, data_folder, parameters)
    return


def split_string_at_last_dot(input_string):
    last_dot_index = input_string.rfind('.')

    if last_dot_index != -1:
        first_part = input_string[:last_dot_index]
        last_part = input_string[last_dot_index + 1:]
        return first_part, last_part
    else:
        # If there is no dot in the input string
        return None, None

if __name__ == '__main__':
    path = str(sys.argv[1])
    execution_folder = str(sys.argv[2])
    data_folder = str(sys.argv[3])
    workflow(path, execution_folder, data_folder)


