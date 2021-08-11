from typing import Union, Generator

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

        Internal representation ._expression set to validated/translated
        form.

        :param new_expression: str
        :return: None
        """
        self._readable_expression = new_expression
        self._expression = pre_parse_translate(new_expression)

    def plot(self, x_min: int = -500,
             x_max: int = 500,
             n: int = None,
             smooth: bool = False,
             very_smooth: bool = False
             ) -> list[tuple[float, Union[int, float]]]:
        """
        Plot expression.

        Generates points.

        Domain x_min/x_max, defaulting to -500/500.

        n - number of points to plot, spread evenly over the domain.
        Defaults to the magnitude of the domain eg ~abs(x_max - x_min).

        smooth/very_smooth: plot given domain with many/very many points
        smooth: 500
        very_smooth 5000

        :param x_min: int
        :param x_max: int
        :param n: int
        :param smooth: bool
        :param very_smooth: bool
        :return: list[tuple[float, Union[int, float]]]
        """
        if n:
            step = (x_max - x_min) / (n - 1)
        elif smooth:
            step = (x_max - x_min) / (500 - 1)
        elif very_smooth:
            step = (x_max - x_min) / (5000 - 1)
        else:
            step = 1
        domain = self.float_range(x_min, x_max + step, step)

        self._parser.evaluate("x=0")

        xy_points = [(x, self._get_y_coord(x)) for x in domain]
        return xy_points

    def _get_y_coord(self, x: Union[int, float]) -> Union[int, float]:
        self._parser.evaluate(f"x={x}")
        return self._parser.evaluate(self._expression)

    @staticmethod
    def float_range(start: Union[int, float],
                    end: Union[int, float],
                    step: Union[int, float] = 1.0
                    ) -> Generator[float, None, None]:
        """
        Range for floats.

        :param start:: Union[int, float]
        :param end:: Union[int, float]
        :param step:: Union[int, float]
        :return: Generator[float, None, None]
        """
        i = 0.0
        x = float(start)
        x0 = x
        half_step = step / 2.0
        yield x
        while x + half_step < end:
            i += 1.0
            x = x0 + i * step  # Multiplication avoids adding floating point errors.
            if x < end:
                yield x
