from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, RationalQuadratic as RQ, ExpSineSquared as Exp, DotProduct, WhiteKernel
from sklearn.gaussian_process.kernels import Matern

def model_creation():