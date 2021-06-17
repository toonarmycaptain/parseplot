"""Test parser.py"""
import pytest

from src.parseplot.parse import parser

from src.parseplot import Parser


def test__init__(monkeypatch):
    def mocked_pre_parse_translate(expression):
        return expression + " translated"

    monkeypatch.setattr(parser, "pre_parse_translate", mocked_pre_parse_translate)

    test_expression = "my test expression"

    test_parser = Parser(test_expression)

    assert test_parser.expression == test_expression
    assert test_parser._expression == mocked_pre_parse_translate(test_expression)


@pytest.mark.parametrize(
    "test_expression, plot_range, points",
    [('3', (-2, 2), [(-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3)]),  # Constant.
     pytest.param("3", (-2, 2), [(-2, 5), (-1, 5), (0, 5), (1, 5), (2, 5)],
                  marks=pytest.mark.xfail(reason="Bad output, test should fail.")),
     pytest.param("3", (-2, 2), [(-5, 2), (-4, 5), (-3, 5), (-2, 5), (-1, 5), (0, 5)],
                  marks=pytest.mark.xfail(reason="Bad range, test should fail.")),
     ('y=3', (-2, 2), [(-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3)]),  # Constant, y=
     ("x+2", (-5, 5), [(x, x + 2) for x in range(-5, 6)]),  # Linear
     ("y=x-2", (-5, 5), [(x, x - 2) for x in range(-5, 6)]),  # Linear, y=
     ("x**2+4", (-5, 5), [(x, x ** 2 + 4) for x in range(-5, 6)]),  # Quadratic
     ("y=x**2-4", (-5, 5), [(x, x ** 2 - 4) for x in range(-5, 6)]),  # Quadratic, y=
     ])
def test_plot(test_expression, plot_range, points):
    test_parser = Parser(test_expression)
    assert test_parser.plot(*plot_range) == points
