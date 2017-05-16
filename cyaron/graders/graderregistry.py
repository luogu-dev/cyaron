class GraderRegistry:
    _registry = dict()

    def grader(self, name):
        def wrapper(func):
            self._registry[name] = func
            return func

        return wrapper

    def invoke(self, name, content, std):
        return self._registry[name](content, std)

    def check(self, name):
        return name in self._registry


CYaRonGraders = GraderRegistry()