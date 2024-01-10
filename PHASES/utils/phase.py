import importlib


def run(phase_function, phase_args, **kwargs):
    module_call, function_call = split_string_at_last_dot(phase_function)
    module = importlib.import_module(module_call)
    return getattr(module, function_call)(phase_args,**kwargs)


def split_string_at_last_dot(input_string):
    last_dot_index = input_string.rfind('.')
    if last_dot_index != -1:
        first_part = input_string[:last_dot_index]
        last_part = input_string[last_dot_index + 1:]
        return first_part, last_part
    else:
        raise ValueError