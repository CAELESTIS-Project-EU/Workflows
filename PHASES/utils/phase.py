import importlib
from PHASES.utils import args_values

def run(phase, inputs, outputs, parameters, data_folder, local_vars, **kwargs):
    try:
        if isinstance(phase, dict):
            phase_info=args_values.get_values(phase, inputs, outputs, parameters, data_folder, local_vars)
            phase_function, phase_args = phase_info
            module_call, function_call = split_string_at_last_dot(phase_function)
            module = importlib.import_module(module_call)
            return getattr(module, function_call)(**phase_args, **kwargs)
        elif isinstance(phase, list) and len(phase)==1:
            phase_info = args_values.get_values(phase, inputs, outputs, parameters, data_folder, local_vars)
            phase_function = phase_info.get("type")
            phase_args = phase_info.get("arguments")
            module_call, function_call = split_string_at_last_dot(phase_function)
            module = importlib.import_module(module_call)
            return getattr(module, function_call)(**phase_args, **kwargs)
        else:
            values="Start"
            for p in phase:
                phase_info = args_values.get_values([p], inputs, outputs, parameters, data_folder, local_vars)
                phase_function = phase_info.get("type")
                phase_args = phase_info.get("arguments")
                print(f"type: {phase_function}, phase_args: {phase_args}")
                module_call, function_call = split_string_at_last_dot(phase_function)
                module = importlib.import_module(module_call)
                values=getattr(module, function_call)(**phase_args, **kwargs)
                print(str(values))
            return values
    except Exception as e:
        raise ValueError(f"An exception occurred: {e}")

def split_string_at_last_dot(input_string):
    last_dot_index = input_string.rfind('.')
    if last_dot_index != -1:
        first_part = input_string[:last_dot_index]
        last_part = input_string[last_dot_index + 1:]
        return first_part, last_part
    else:
        raise ValueError(f"An exception occurred: split_string_at_last_dot")
