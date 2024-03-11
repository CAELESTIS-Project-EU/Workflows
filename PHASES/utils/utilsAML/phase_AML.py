import importlib


def run(phase_info, **kwargs):
    # Assuming phase_info is a tuple (phase_function, phase_args)
    if len(phase_info) != 2:
        raise ValueError("Invalid phase_info tuple. Expected (phase_function, phase_args).")
    if isinstance(phase_info, dict):
        phase_function= phase_info.get("type")
        phase_args=phase_info.get("arguments")
        module_call, function_call = split_string_at_last_dot(phase_function)
        module = importlib.import_module(module_call)
        return getattr(module, function_call)(**phase_args, **kwargs)
    else:
        values=[]
        for phase in phase_info:
            phase_function = phase.get("type")
            phase_args = phase.get("arguments")
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