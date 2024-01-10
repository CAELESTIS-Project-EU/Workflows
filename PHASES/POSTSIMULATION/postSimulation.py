import importlib
import os.path

from pycompss.api.task import task
from pycompss.api.parameter import *


@task(returns=1)
def collect(post_process_type, post_process_args, out):
    module_call, function_call = split_string_at_last_dot(post_process_type)
    module = importlib.import_module(module_call)
    y = getattr(module, function_call)(post_process_args)
    return y


@task(y_param=COLLECTION_IN)
def write_file(write_file_type, write_file_args, **kwargs):
    module_call, function_call = split_string_at_last_dot(write_file_type)
    module = importlib.import_module(module_call)
    getattr(module, function_call)(write_file_args)
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