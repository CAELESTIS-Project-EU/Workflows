from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, RationalQuadratic as RQ, ExpSineSquared as Exp, DotProduct, WhiteKernel
from sklearn.gaussian_process.kernels import Matern

def training(X,y):
    kernel = C(0.1, (1e-5, 10000)) * 2**2* DotProduct(sigma_0=0.1,  sigma_0_bounds=(1, 10))
    gpr = GaussianProcessRegressor(kernel=kernel,random_state = 0).fit(X, y)
    gpr.predict(X[:2, :], return_std=True)
    return