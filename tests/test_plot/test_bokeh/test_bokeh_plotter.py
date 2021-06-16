"""Test bokeh_plotter.py"""
from pathlib import Path

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


class TestSaveHtmlToFile:
    @pytest.mark.parametrize(
        'filepath, used_filepath',
        [  # str
            ('some_filename', 'some_filename.html'),  # filename w/o ext
            ('some_filename.html', 'some_filename.html'),  # filename w/correct ext
            ('some_filename.other_ext', 'some_filename.other_ext.html'),  # filename w/wrong ext
            pytest.param('some_filename.bad', 'some_filename.worse',
                         marks=pytest.mark.xfail(reason="Sanity check; wrong output.")),
            # pathlib.Path
            (Path('some_filename'), Path('some_filename.html')),  # filename w/o ext
            (Path('some_filename.html'), Path('some_filename.html')),  # filename w/correct ext
            (Path('some_filename.other_ext'), Path('some_filename.other_ext.html')),  # filename w/wrong ext
            pytest.param(Path('some_filename.bad'), Path('some_filename.worse'),
                         marks=pytest.mark.xfail(reason="Sanity check; wrong output.")),
        ])
    def test_save_html_to_file(self, monkeypatch, filepath, used_filepath):
        test_plotter = BokehPlotter()
        test_filepath = filepath

        # mock test_plotter._plot
        test__plot = 'a test plot'
        test_plotter._plot = test__plot

        # Mock bokeh.io.save
        mocked_save_called = False

        def mock_save(plot, filename):
            nonlocal mocked_save_called
            mocked_save_called = True
            assert plot is test__plot
            assert filename == used_filepath
            return filename

        monkeypatch.setattr(bokeh_plotter, 'save', mock_save)

        assert test_plotter.save_html_to_file(test_filepath) == used_filepath

        assert mocked_save_called


class TestSaveAsPng:
    @pytest.mark.parametrize(
        'filepath, used_filepath',
        [  # str
            ('some_filename', 'some_filename.png'),  # filename w/o ext
            ('some_filename.png', 'some_filename.png'),  # filename w/correct ext
            ('some_filename.other_ext', 'some_filename.other_ext.png'),  # filename w/wrong ext
            pytest.param('some_filename.bad', 'some_filename.worse',
                         marks=pytest.mark.xfail(reason="Sanity check; wrong output.")),
            # pathlib.Path
            (Path('some_filename'), Path('some_filename.png')),  # filename w/o ext
            (Path('some_filename.png'), Path('some_filename.png')),  # filename w/correct ext
            (Path('some_filename.other_ext'), Path('some_filename.other_ext.png')),  # filename w/wrong ext
            pytest.param(Path('some_filename.bad'), Path('some_filename.worse'),
                         marks=pytest.mark.xfail(reason="Sanity check; wrong output.")),
        ])
    def test_save_as_png(self, monkeypatch, filepath, used_filepath):
        test_plotter = BokehPlotter()
        test_filepath = filepath

        # mock test_plotter._plot
        test__plot = 'a test plot'
        test_plotter._plot = test__plot

        # Mock __initialise_webdriver
        mocked__initialise_webdriver_called = False
        mock___initialise_webdriver_return = 'mocked__initialise_webdriver_called'

        def mock___initialise_webdriver():
            nonlocal mocked__initialise_webdriver_called
            mocked__initialise_webdriver_called = True
            return mock___initialise_webdriver_return

        test_plotter._BokehPlotter__initialise_webdriver = mock___initialise_webdriver

        # Mock bokeh.io.save
        mocked_export_png = False

        def mock_export_png(plot, filename, webdriver):
            nonlocal mocked_export_png
            mocked_export_png = True
            assert plot is test__plot
            assert filename == used_filepath
            assert webdriver == mock___initialise_webdriver_return
            return filename

        monkeypatch.setattr(bokeh_plotter, 'export_png', mock_export_png)

        assert test_plotter.save_as_png(test_filepath) == used_filepath

        assert mocked_export_png
        assert mocked__initialise_webdriver_called


class TestSaveAsSvg:
    @pytest.mark.parametrize(
        'filepath, used_filepath',
        [  # str
            ('some_filename', 'some_filename.svg'),  # filename w/o ext
            ('some_filename.svg', 'some_filename.svg'),  # filename w/correct ext
            ('some_filename.other_ext', 'some_filename.other_ext.svg'),  # filename w/wrong ext
            pytest.param('some_filename.bad', 'some_filename.worse',
                         marks=pytest.mark.xfail(reason="Sanity check; wrong output.")),
            # pathlib.Path
            (Path('some_filename'), Path('some_filename.svg')),  # filename w/o ext
            (Path('some_filename.svg'), Path('some_filename.svg')),  # filename w/correct ext
            (Path('some_filename.other_ext'), Path('some_filename.other_ext.svg')),  # filename w/wrong ext
            pytest.param(Path('some_filename.bad'), Path('some_filename.worse'),
                         marks=pytest.mark.xfail(reason="Sanity check; wrong output.")),
        ])
    def test_save_as_svg(self, monkeypatch, filepath, used_filepath):
        test_plotter = BokehPlotter()
        test_filepath = filepath

        # mock test_plotter._plot
        test__plot = 'a test plot'
        test_plotter._plot = test__plot

        # Mock __initialise_webdriver
        mocked__initialise_webdriver_called = False
        mock___initialise_webdriver_return = 'mocked__initialise_webdriver_called'

        def mock___initialise_webdriver():
            nonlocal mocked__initialise_webdriver_called
            mocked__initialise_webdriver_called = True
            return mock___initialise_webdriver_return

        test_plotter._BokehPlotter__initialise_webdriver = mock___initialise_webdriver

        # Mock bokeh.io.save
        mocked_export_svg = False

        def mock_export_svg(plot, filename, webdriver):
            nonlocal mocked_export_svg
            mocked_export_svg = True
            assert plot is test__plot
            assert filename == used_filepath
            assert webdriver == mock___initialise_webdriver_return
            return filename

        monkeypatch.setattr(bokeh_plotter, 'export_svg', mock_export_svg)

        assert test_plotter.save_as_svg(test_filepath) == used_filepath

        assert mocked_export_svg
        assert mocked__initialise_webdriver_called


class TestShowInBrowser:
    def test_show_in_browser(self, monkeypatch):
        test_plotter = BokehPlotter()

        # Mock ._plot
        test__plot = 'a dummy plot'
        test_plotter._plot = test__plot

        # mock bokeh.io.show
        mocked_show_called = False

        def mock_show(plot):
            nonlocal mocked_show_called
            mocked_show_called = True
            assert plot == test__plot

        monkeypatch.setattr(bokeh_plotter, 'show', mock_show)

        assert test_plotter.show_in_browser() is None

        assert mocked_show_called


class TestAddLines:
    @pytest.mark.parametrize(
        'lines, number_of_lines',
        [([(x, x + 1) for x in range(5)], 1),  # single line of points
         ([[(x, x + 1) for x in range(5)]], 1),  # Single line nested as if multiple.
         ([[(x, x + 1) for x in range(5)], [(x, x + 1) for x in range(10)]], 2),  # multiple lines
         (['one', 'two', 'three', 'four', 'five'], 5),
         pytest.param([[(x, x + 1) for x in range(5)], [(x, x + 1) for x in range(10)]], 1,
                      marks=pytest.mark.xfail(reason="Sanity check; wrong output.")),
         pytest.param([(x, x + 1) for x in range(5)], 2,
                      marks=pytest.mark.xfail(reason="Sanity check; wrong output.")),
         pytest.param(['one', 'two', 'three'], 7,
                      marks=pytest.mark.xfail(reason="Sanity check; wrong output.")),
         ])
    def test___add_lines(self, lines, number_of_lines):
        test_plotter = BokehPlotter()

        # Mock .add_line
        mocked_add_line_calls = []

        def mock_add_line(points):
            nonlocal mocked_add_line_calls
            mocked_add_line_calls.append(points)

        test_plotter.add_line = mock_add_line

        assert test_plotter._BokehPlotter__add_lines(lines) is None
        assert len(mocked_add_line_calls) == number_of_lines
