"""Test parser.py"""
import pytest

from src.parseplot.parse import parser

from src.parseplot import Parser


def test__init__(monkeypatch):
    test_expression = "my test expression"
    test_translated_expression = test_expression + " translated"

    def mocked_pre_parse_translate(expression):
        return test_translated_expression

    monkeypatch.setattr(parser, "pre_parse_translate", mocked_pre_parse_translate)

    test_parser = Parser(test_expression)

    assert test_parser.expression == test_expression
    assert test_parser._readable_expression == test_expression
    assert test_parser._expression == test_translated_expression


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


def test_plot_default_args():
    x_min = -500
    x_max = 500

    test_parser = Parser('x**2')
    points = test_parser.plot()

    assert x_min == points[0][0]
    assert x_max == points[-1][0]
    assert 500 == points[1000][0]  # ie 1001st point x value is x_max.
    assert len(points) == (x_max - x_min) + 1


@pytest.mark.parametrize(
    "test_expression, plot_args, num_points",
    [("x**2+4", {'x_min': -5, 'x_max': 5}, 11),  # default 1 per min-max + 1
     pytest.param("x**2+4", {'x_min': -5, 'x_max': 5}, 27,
                  marks=pytest.mark.xfail(reason="Wrong number of points, test should fail.")),
     ("x**2+4", {'x_min': 10, 'x_max': 20}, 11),
     # n points
     ("x**2+4", {'x_min': -5, 'x_max': 5}, 11),  # default 1 per min-max + 1
     pytest.param("x**2+4", {'x_min': -5, 'x_max': 5}, 27,
                  marks=pytest.mark.xfail(reason="Wrong number of points, test should fail.")),
     ("x**2+4", {'x_min': 10, 'x_max': 25}, 16),
     # n=0 is ignored
     ("x**2+4", {'x_min': -5, 'x_max': 5, 'n': 0}, 11),
     pytest.param("x**2+4", {'x_min': -5, 'x_max': 5, 'n': 0}, 0,
                  marks=pytest.mark.xfail(reason="n=0 not ignored, test should fail.")),
     # smooth
     ("x**2+4", {'x_min': -5, 'x_max': 5, 'smooth': True}, 500),
     # very smooth
     ("x**2+4", {'x_min': -5, 'x_max': 5, 'very_smooth': True}, 5000),
     # n taking precedence over smooth/very_smooth
     ("x**2+4", {'x_min': -5, 'x_max': 5, 'n': 5, 'smooth': True}, 5),
     ("x**2+4", {'x_min': -5, 'x_max': 5, 'n': 5, 'very_smooth': True}, 5),
     # smooth taking precedence over very_smooth
     ("x**2+4", {'x_min': -5, 'x_max': 5, 'smooth': True, 'very_smooth': True}, 500),
     ])
def test_plot_n_smooth_very_smooth_args(test_expression, plot_args, num_points):
    test_parser = Parser(test_expression)
    assert len(test_parser.plot(**plot_args)) == num_points
