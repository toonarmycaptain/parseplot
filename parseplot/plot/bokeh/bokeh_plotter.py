"""Bokeh plotter"""
from pathlib import Path
from typing import Union, Sequence, Optional

import PIL
from bokeh import io
from bokeh.io import show
from bokeh.plotting import figure


class BokehPlotter:
    """Plotter wrapping Bokeh"""

    def __init__(self,
                 points: Union[Sequence[tuple[int, float]],
                               Sequence[Sequence[tuple[int, float]]]] = None,
                 *,
                 title: str = None,
                 x_axis_label: str = None,
                 y_axis_label: str = None,
                 ) -> None:
        """
        Object wrapping bokeh plotting functionality.

        May be initialised with a list of points, or a list of lists of points,
        as well as plot data such as title, axis labels.

        Plot data other than a list of points must be passed via kw arguments,
        to allow for BokehPlotter([list of points])
                  or BokehPlotter(title='title,
                                  x_axis_label: str = None,
                                  y_axis_label: str = None,
                                  points=[list of points])
                  or BokehPlotter[[list of points], title='title')
        calling formats.

        points must be a sequence, or sequence of sequences of of x,y tuples of int or float.

        :param points: Sequence[Sequence[tuple[int, float]]]
        """
        self.title: Optional[str] = title
        self.x_axis_label: Optional[str] = x_axis_label
        self.y_axis_label: Optional[str] = y_axis_label
        self._plot: figure = figure(title=self.title,
                                    x_axis_label=x_axis_label,
                                    y_axis_label=self.y_axis_label)
        self.points: list[Sequence[tuple[int, float]]] = []
        if points:
            self.__add_lines(points)

        self.plotted = None

    def add_line(self,
                 points: Sequence[tuple[int, float]],
                 legend_label: str = None,
                 line_color: str = None,
                 line_width: int = None,
                 ):
        """

        :param points:
        :param legend_label:
        :param line_color:
        :param line_width:
        """
        self.points.append(points)
        line_args = {'x': [x[0] for x in points],
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
             passed_points: list[tuple[int, float]] = None,
             ) -> PIL.Image:
        """
        Plots the class' points, adding a line if points are passed.


        :param passed_points:
        :return:
        """
        if passed_points:
            self.add_line(passed_points)

        # need browser installed?
        # self.plotted = io.export.get_screenshot_as_png(self._plot)
        # return self.plotted
        return show(self._plot)

    def save_to_file(self, filepath: Union[Path, str] = None) -> str:
        """
        Save the plot to the given filepath.
        :param filepath:
        :return:
        """
        return io.save(self._plot, filename=filepath)

    def __add_lines(self, points: Union[Sequence[tuple[int, float]],
                                        Sequence[Sequence[tuple[int, float]]]]) -> None:
        """
        Parse passed in points into plot lines, multiple times if data is a
        series of lists of points.

        :param points:
        :return:
        """
        try:
            points[0][0][0]  # Will throw an exception if only one sequence of xy tuples.
            # Multiple lists of points.
            for line in points:
                self.add_line(line)
        except TypeError:  # Single list:
            self.add_line(points)
