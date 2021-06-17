from plusminus import ArithmeticParser

from .pre_parse import pre_parse_translate


class Parser:
    """
    parseplot parser class
    """

    def __init__(self, expression: str):
        self.expression = expression
        self._parser = ArithmeticParser()

    @property
    def expression(self):
        """Returns the given expression."""
        return self._readable_expression

    @expression.setter
    def expression(self, new_expression: str):
        """
        Reassigns ._readable_expression, ._expression

        Internal representation ._expression set to validated/translated form.

        :param new_expression: str
        :return: None
        """
        self._readable_expression = new_expression
        self._expression = pre_parse_translate(new_expression)

    def plot(self, x_min: int = -500, x_max: int = 500) -> list[tuple[int, float]]:
        """
        Plot expression.

        :param x_min: int
        :param x_max: int
        :return: list[tuple]
        """
        self._parser.evaluate("x=0")

        xy_points: list[tuple[int, float]] = []
        for x in range(x_min, x_max + 1):
            self._parser.evaluate(f"x={x}")
            xy = (x, self._parser.evaluate(self._expression))
            xy_points.append(xy)
        return xy_points
