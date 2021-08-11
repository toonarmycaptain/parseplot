"""Bokeh plotter"""
from __future__ import annotations
from pathlib import Path
from typing import (Any,
                    Optional,
                    Sequence,
                    TYPE_CHECKING,
                    Union,
                    )

import PIL
from bokeh.io.export import get_screenshot_as_png
from bokeh.io import (export_png,
                      export_svg,
                      save,
                      show,
                      )
from bokeh.plotting import figure

from src.parseplot.util.filepath_helpers import ensure_extension

if TYPE_CHECKING:
    from selenium import webdriver


class BokehPlotter:
    """Plotter wrapping Bokeh"""

    def __init__(self,
                 points: Union[Sequence[tuple[Union[int, float], Union[int, float]]],
                               Sequence[Sequence[tuple[Union[int, float], Union[int, float]]]]] = None,
                 *,
                 title: str = None,
                 x_axis_label: str = None,
                 y_axis_label: str = None,
                 x_axis_location: Union[int, float] = None,
                 y_axis_location: Union[int, float] = None,
                 ) -> None:
        """
        Object wrapping bokeh plotting functionality.

        May be initialised with a list of points, or a list of lists of
        points,
        as well as plot data such as title, axis labels.

        Plot data other than a list of points must be passed via kw
        arguments,to allow for BokehPlotter([list of points])
                            or BokehPlotter(title='title,
                                            x_axis_label: str = None,
                                            y_axis_label: str = None,
                                            points=[list of points])
                            or BokehPlotter([list of points],
                                            title='title')
        calling formats.

        points must be a sequence, or sequence of sequences of of x,y
        tuples of int or float.

        Plots may be constructed via the class constructor:
            >>> b = BokehPlotter(title="Test plot",
            >>>                  x_axis_label='x axis',
            >>>                  y_axis_label='vertical axis',
            >>>                  x_axis_location=0,
            >>>                  y_axis_location=0,
            >>>                  points=[[(x / 10, (x / 10) ** 2 - 4) for x in range(-50, 60)],
            >>>                          [(x / 10, (x / 10) ** 3) for x in range(-30, 40)],
            >>>                          [(x, x + 10) for x in range(-15, 16)]
            >>>                          ])

        Or procedurally:
            >>> b = BokehPlotter(title="Test_plot")
            >>> b.x_axis_label = 'x axis'
            >>> b.y_axis_label = 'y axis'
            >>> b.x_axis_location, b.y_axis_location = (0, 0)
            >>> b.add_line([(x / 10, (x / 10) ** 2 - 4) for x in range(-50, 60)])
            >>> b.add_line([(x / 10, (x / 10) ** 3) for x in range(-30, 40)])
            >>> b.add_line([(x, x + 10) for x in range(-15, 16)])


        :param points: Union[Sequence[tuple[int, float]],
                               Sequence[Sequence[tuple[int, float]]]]

        :param title: str title for chart
        :param x_axis_label: str label for x axis
        :param y_axis_label: str label for y axis
        :param x_axis_location: int location of x-axis (on y-axis)
        :param y_axis_location: int location of y-axis (on x-axis)
        :return: None
        """
        self._plot: figure = figure()

        self.title: Optional[str] = title
        self.x_axis_label: Optional[str] = x_axis_label
        self.y_axis_label: Optional[str] = y_axis_label
        self.x_axis_location: Optional[Union[int, float]] = x_axis_location
        self.y_axis_location: Optional[Union[int, float]] = y_axis_location

        self.points: list[Sequence[tuple[Union[int, float], Union[int, float]]]] = []
        if points:
            self.__add_lines(points)

    @property
    def title(self):
        return self._plot.title

    @title.setter
    def title(self, new_title):
        self._plot.title = new_title

    @property
    def x_axis_label(self):
        return self._plot.xaxis.axis_label

    @x_axis_label.setter
    def x_axis_label(self, new_x_axis_label):
        self._plot.xaxis.axis_label = new_x_axis_label

    @property
    def y_axis_label(self):
        return self._plot.yaxis.axis_label

    @y_axis_label.setter
    def y_axis_label(self, new_y_axis_label):
        self._plot.yaxis.axis_label = new_y_axis_label

    @property
    def x_axis_location(self):
        return self._plot.xaxis.fixed_location

    @x_axis_location.setter
    def x_axis_location(self, new_x_axis_location):
        self._plot.xaxis.fixed_location = new_x_axis_location

    @property
    def y_axis_location(self):
        return self._plot.yaxis.fixed_location

    @y_axis_location.setter
    def y_axis_location(self, new_y_axis_location):
        self._plot.yaxis.fixed_location = new_y_axis_location

    def add_line(self,
                 points: Sequence[tuple[Union[int, float], Union[int, float]]],
                 legend_label: str = None,
                 line_color: str = None,
                 line_width: int = None,
                 ) -> None:
        """
        Add a line to the class' plot.

        :param points: Sequence[tuple[int, float]]
        :param legend_label: str
        :param line_color: str
        :param line_width: str
        :return: None
        """
        self.points.append(points)
        line_args: dict[str, Any] = {'x': [x[0] for x in points],
                                     'y': [y[1] for y in points],
                                     }
        if legend_label:
            line_args['legend_label'] = legend_label
        if line_color:
            line_args['line_color'] = line_color
        if line_width:
            line_args['line_width'] = line_width
        self._plot.line(**line_args)

    def plot(self,
             passed_points: Sequence[tuple[int, float]] = None,
             ) -> None:
        """
        Show plot in browser, adding a line if points are passed.

        :param passed_points: Sequence[tuple[int, float]]
        :return: None
        """
        if passed_points:
            self.add_line(passed_points)

        return self.show_in_browser()

    def plot_PIL_Image_png(self) -> PIL.Image:
        """
        Returns plot as a PIL Image object

        :return: PIL.Image object
        """
        return get_screenshot_as_png(self._plot,
                                     driver=self.__initialise_webdriver())

    def save_html_to_file(self, filepath: Union[str, Path]
                          ) -> Union[str, Path]:
        """
        Save the html plot to the given filepath.

        Appends .html extension if not given.

        :param filepath: str
        :return: str|Path
        """
        extension = '.html'

        filepath = ensure_extension(filepath, extension)
        return save(self._plot, filename=filepath)

    def save_as_png(self, filepath: Union[str, Path]) -> Union[str, Path]:
        """
        Save the plot to the given filepath as a png image.

        Appends .png extension if not given.

        export_png returns a list of strings, this taking first element
        returns just the filepath

        :param filepath: Path|str
        :return: Path|str
        """
        extension = '.png'

        filepath = ensure_extension(filepath, extension)
        export_png(self._plot, filename=filepath, webdriver=self.__initialise_webdriver())

        return filepath

    def save_as_svg(self, filepath: Union[str, Path]) -> Union[str, Path]:
        """
        Save the plot to the given filepath as a svg image.

        Appends .svg extension if not given.

        export_svg returns a list of strings, this taking first element
        returns just the filepath

        :param filepath: Path|str
        :return: Path|str
        """
        extension = '.svg'

        filepath = ensure_extension(filepath, extension)
        export_svg(self._plot, filename=filepath, webdriver=self.__initialise_webdriver())

        return filepath

    def show_in_browser(self) -> None:
        """
        Shows plot in default browser.

        :return: None
        """
        show(self._plot)

    def __add_lines(self, points: Union[Sequence[tuple[Union[int, float], Union[int, float]]],
                                        Sequence[Sequence[tuple[Union[int, float], Union[int, float]]]]]) -> None:
        """
        Parse passed in points into plot lines, multiple times if data
        is a series of lists of points.

        :param points: Union[Sequence[tuple[Union[int, float], Union[int, float]]],
                             Sequence[Sequence[tuple[Union[int, float], Union[int, float]]]]]
        :return: None
        """
        if isinstance(points[0][0], Sequence):  # Multiple lists of points.
            lines: Sequence[Sequence[tuple[Union[int, float], Union[int, float]]]] = points  # type: ignore
            for line in lines:
                self.add_line(line)
        else:  # Single list:
            line: Sequence[tuple[Union[int, float], Union[int, float]]] = points  # type: ignore
            self.add_line(line)

    @staticmethod
    def __initialise_webdriver() -> webdriver.Firefox:
        """
        Returns initialised Firefox webdriver.

        Very slow.
        Requires Firefox to be installed.

        :return: webdriver.Firefox
        """
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        import geckodriver_autoinstaller

        geckodriver_autoinstaller.install()  # In case driver not installed.
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        return driver
