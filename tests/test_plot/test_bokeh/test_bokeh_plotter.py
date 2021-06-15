import pytest

from src.parseplot.plot.bokeh import bokeh_plotter
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


class TestBokehPlotterAttrs:
    def test_title(self):
        test_title = 'some title'
        test_plotter = BokehPlotter(title=test_title)
        assert test_plotter.title == test_title

    def test_x_axis_label(self):
        test_x_axis_label = 'some x_axis_label'
        test_plotter = BokehPlotter(x_axis_label=test_x_axis_label)
        assert test_plotter.x_axis_label == test_x_axis_label

    def test_y_axis_label(self):
        test_y_axis_label = 'some y_axis_label'
        test_plotter = BokehPlotter(y_axis_label=test_y_axis_label)
        assert test_plotter.y_axis_label == test_y_axis_label

    def test_x_axis_location(self):
        test_x_axis_location = 'some x_axis_location'
        test_plotter = BokehPlotter(x_axis_location=test_x_axis_location)
        assert test_plotter.x_axis_location == test_x_axis_location

    def test_y_axis_location(self):
        test_y_axis_location = 'some y_axis_location'
        test_plotter = BokehPlotter(y_axis_location=test_y_axis_location)
        assert test_plotter.y_axis_location == test_y_axis_location


class TestAddLine:
    def test_add_line_args_forwarded(self):
        """Simple test that points/args are forwarded to self._plot.line()"""
        test_points = [(1, 2), (3, 4), (5, 6)]
        test_x_points = [1, 3, 5]
        test_y_points = [2, 4, 6]
        test_legend_label = 'test_legend_label'
        test_line_color = 'test_line_color'
        test_line_width = 314

        test_plotter = BokehPlotter()

        # patch _plot.line
        class TestPlotLine:
            def line(self, **args):
                print(args)
                assert args['x'] == test_x_points
                assert args['y'] == test_y_points
                assert args['legend_label'] == test_legend_label
                assert args['line_color'] == test_line_color
                assert args['line_width'] == test_line_width

        test_plotter._plot = TestPlotLine()

        test_plotter.add_line(points=test_points,
                              legend_label=test_legend_label,
                              line_color=test_line_color,
                              line_width=test_line_width,
                              )


class TestPlot:
    @pytest.mark.parametrize(
        'points',  # points/new line added
        [None,  # no points/new line added
         [(1, 2), (3, 4), (5, 6)]
         ])
    def test_points_added(self, points):
        test_plotter = BokehPlotter()

        # patch add_line method
        add_line_called = False

        def add_line_telemetry(*args, **kwargs):
            nonlocal add_line_called  # Needed to assign var in scope
            add_line_called = True

        test_plotter.add_line = add_line_telemetry

        # patch show_in_browser method
        test_plotter.show_in_browser = lambda: None

        test_plotter.plot(points)
        assert add_line_called == bool(points)


class TestPlotPILImagePNG:
    def test_plot_PIL_Image_png_mocked(self, monkeypatch):
        test_plotter = BokehPlotter()

        # Mock plot
        test__plot = 'a test plot'
        test_plotter._plot = test__plot

        # Mock get_screenshot_as_png
        mocked_get_screenshot_as_png = False
        mock_get_screenshot_as_png_return = "mocked_get_screenshot_as_png_called"

        def mock_get_screenshot_as_png(*args, **kwargs):
            nonlocal mocked_get_screenshot_as_png
            mocked_get_screenshot_as_png = True
            assert test_plotter._plot in args
            assert kwargs['driver'] == test_plotter._BokehPlotter__initialise_webdriver()
            return mock_get_screenshot_as_png_return

        monkeypatch.setattr(bokeh_plotter, 'get_screenshot_as_png', mock_get_screenshot_as_png)

        # Mock __initialise_webdriver
        mocked__initialise_webdriver_called = False
        mock___initialise_webdriver_return = 'mocked__initialise_webdriver_called'

        def mock___initialise_webdriver():
            nonlocal mocked__initialise_webdriver_called
            mocked__initialise_webdriver_called = True
            return mock___initialise_webdriver_return

        test_plotter._BokehPlotter__initialise_webdriver = mock___initialise_webdriver

        assert test_plotter.plot_PIL_Image_png() == mock_get_screenshot_as_png_return
        # Ensure expected calls
        assert mocked_get_screenshot_as_png
        assert mocked__initialise_webdriver_called
