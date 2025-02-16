from typing import Callable, Tuple, Dict, Union

__all__ = ['CYaRonGraders', 'GraderType']

GraderType = Callable[[str, str], Tuple[bool, Union[str, None]]]


class GraderRegistry:
    """A registry for grader functions."""
    _registry: Dict[str, GraderType] = {}

    def grader(self, name: str):
        """A decorator to register a grader function."""

        def wrapper(func: GraderType):
            self._registry[name] = func
            return func

        return wrapper

    def invoke(self, grader: Union[str, GraderType], content: str, std: str):
        """Invoke a grader function by name or function object."""
        if isinstance(grader, str):
            return self._registry[grader](content, std)
        else:
            return grader(content, std)

    def check(self, name):
        """Check if a grader is registered."""
        return name in self._registry


CYaRonGraders = GraderRegistry()
