import pytest

from src.parseplot.plot.bokeh.bokeh_plotter import BokehPlotter


@pytest.mark.parametrize(
    'test_points, points_attr',
    [([[(1, 2), (3, 4), (5, 6)]], [[(1, 2), (3, 4), (5, 6)]]),  # Points passed.
     ([[(1, 2), (3, 4)], [(5, 6), (7, 8)], [(9, 10), (11, 12)]],
      [[(1, 2), (3, 4)], [(5, 6), (7, 8)], [(9, 10), (11, 12)]]),  # Two lines.
     (None, list()),  # Default argument
     ])
def test__init__(test_points, points_attr):
    test_plotter = BokehPlotter(test_points)
    assert test_plotter.points == points_attr
