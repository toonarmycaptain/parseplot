"""Test pre_parse.py"""
import pytest

from src.parseplot.parse.pre_parse import pre_parse_translation


class TestPreParseTranslation:
    @pytest.mark.parametrize(
        "input_function, output_function",
        [
            ("x**2+4", "x**2+4"),
            ("x^2+4", "x**2+4"),  # ^ power replaced by **
            ("y=x^2+4", "y=x**2+4"),
            pytest.param(
                "x^2+4",
                "x^2+4",
                marks=pytest.mark.xfail(reason="Bad output, test should fail."),
            ),
        ],
    )
    def test_pre_parse_translation(self, input_function, output_function):
        assert pre_parse_translation(input_function) == output_function
