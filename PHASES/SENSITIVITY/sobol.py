from SALib.analyze import sobol as sobolAnalyze

def sobol(problem, y, param_values, output_file, **kwargs):
    Si = sobolAnalyze.analyze(problem, y)
    return Si