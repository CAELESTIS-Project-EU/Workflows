from sklearn.gaussian_process.kernels import ConstantKernel, DotProduct


def gen_param(**kwargs):
    parameters = kwargs.get("parameters")
    constant_value = float(parameters['constant_value'])
    sigma0 = float(parameters['sigma0'])
    # Extracting constant_bounds
    constant_bounds = parameters['sigma_0_bounds']
    constant_min = constant_bounds[0]['min']
    constant_max = constant_bounds[1]['max']

    # Extracting sigma_0_bounds
    sigma_0_bounds = parameters['sigma_0_bounds']
    sigma_0_min = sigma_0_bounds[0]['min']
    sigma_0_max = sigma_0_bounds[1]['max']

    return ConstantKernel(constant_value, (constant_min, constant_max)) * 2 ** 2 * DotProduct(
        sigma_0=sigma0, sigma_0_bounds=(sigma_0_min, sigma_0_max))
