"""Test parser.py"""
import pytest

from parseplot.parse import parser

from parseplot.parse import Parser


def test__init__(monkeypatch):
    def mocked_pre_parse_translation(function):
        return function + " translated"

    monkeypatch.setattr(parser, "pre_parse_translation", mocked_pre_parse_translation)

    test_function = "my test function"

    test_parser = Parser(test_function)

    assert test_parser.function == test_function
    assert test_parser._function == mocked_pre_parse_translation(test_function)


@pytest.mark.parametrize(
    "test_function, plot_range, points",
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
def test_plot(test_function, plot_range, points):
    test_parser = Parser(test_function)
    assert test_parser.plot(*plot_range) == points
