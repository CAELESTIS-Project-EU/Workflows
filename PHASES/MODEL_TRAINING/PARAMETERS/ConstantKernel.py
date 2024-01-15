from sklearn.gaussian_process.kernels import ConstantKernel, DotProduct

@task(returns=1)
def gen_param(kernel_args, **kwargs):
    constant_value = float(get_value(kernel_args, "constant_value"))
    sigma0 = float(get_value(kernel_args, "sigma0"))
    # Extracting constant_bounds
    constant_bounds = get_value(kernel_args, "constant_bounds")
    constant_min = constant_bounds[0]['min']
    constant_max = constant_bounds[1]['max']

    # Extracting sigma_0_bounds
    sigma_0_bounds = get_value(kernel_args, "sigma_0_bounds")
    sigma_0_min = sigma_0_bounds[0]['min']
    sigma_0_max = sigma_0_bounds[1]['max']

    return ConstantKernel(constant_value, (constant_min, constant_max)) * 2 ** 2 * DotProduct(
        sigma_0=sigma0, sigma_0_bounds=(sigma_0_min, sigma_0_max))


def get_value(element, param):
    if param in element:
        return element[param]
    else:
        raise ValueError(f"The key '{param}' was not found in the dictionary.")
