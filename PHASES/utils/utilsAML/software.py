
class Software:

    def __init__(self, module, function, parameters) -> None:
        self.module=module
        self.function=function
        self.parameters=parameters

    def get_function(self):
        return self.function

    def get_parameters(self):
        return self.parameters

    def get_module(self):
        return self.module