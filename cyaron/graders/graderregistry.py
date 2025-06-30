from typing import Callable, Tuple, Dict, Union, Any

__all__ = ['CYaRonGraders', 'GraderType2', 'GraderType3']

GraderType2 = Callable[[str, str], Tuple[bool, Any]]
GraderType3 = Callable[[str, str, str], Tuple[bool, Any]]


class GraderRegistry:
    """A registry for grader functions."""
    _registry: Dict[str, GraderType3] = {}

    def grader2(self, name: str):
        """
        This decorator registers a grader function under a specific name in the registry.
        
        The function being decorated should accept exactly two parameters (excluding 
        the content input).
        """

        def wrapper(func: GraderType2):
            self._registry[name] = lambda content, std, _: func(content, std)
            return func

        return wrapper

    grader = grader2

    def grader3(self, name: str):
        """
        This decorator registers a grader function under a specific name in the registry.
        
        The function being decorated should accept exactly three parameters.
        """

        def wrapper(func: GraderType3):
            self._registry[name] = func
            return func

        return wrapper

    def invoke(self, grader: Union[str, GraderType3], content: str, std: str,
               input_content: str):
        """Invoke a grader function by name or function object."""
        if isinstance(grader, str):
            return self._registry[grader](content, std, input_content)
        else:
            return grader(content, std, input_content)

    def check(self, name: str):
        """Check if a grader is registered."""
        return name in self._registry


CYaRonGraders = GraderRegistry()
