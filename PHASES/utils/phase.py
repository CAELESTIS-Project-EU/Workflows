import importlib
from PHASES.utils import args_values

def run(phase, inputs, outputs, parameters, data_folder, local_vars, **kwargs):
    print(f"phase: {phase}")
    print(f"inputs: {inputs}")
    print(f"outputs: {outputs}")
    print(f"parameters: {parameters}")
    print(f"data_folder: {data_folder}")
    print(f"local_vars: {local_vars}")
    # Assuming phase_info is a tuple (phase_function, phase_args)
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
        values = []
        for p in phase:
            phase_info = args_values.get_values([p], inputs, outputs, parameters, data_folder, local_vars)
            phase_function = phase_info.get("type")
            phase_args = phase_info.get("arguments")
            #phase_args =args_values.get_values(phase_info, inputs, outputs, parameters, data_folder, local_vars)
            module_call, function_call = split_string_at_last_dot(phase_function)
            module = importlib.import_module(module_call)
            values.append(getattr(module, function_call)(**phase_args, **kwargs))
        return values

def split_string_at_last_dot(input_string):
    last_dot_index = input_string.rfind('.')
    if last_dot_index != -1:
        first_part = input_string[:last_dot_index]
        last_part = input_string[last_dot_index + 1:]
        return first_part, last_part
    else:
        raise ValueError
