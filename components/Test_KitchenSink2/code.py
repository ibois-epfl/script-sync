"""
Do something silly.

This component does nothing useful, it's only a kitchen sink example showing most available options.

    Args:
        x: X value
        y: Y value
        z: Z value
    Returns:
        result: The sum of all three values.
"""
from ghpythonlib.componentbase import executingcomponent as component


class KitchenSinkComponent(component):
    def RunScript(self, x, y, z):
        self.Message = 'COMPONENT v{{version}}'
        return x + y + z