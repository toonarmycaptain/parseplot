from pathlib import Path

import pytest

from src.parseplot.util.filepath_helpers import ensure_extension


@pytest.mark.parametrize(
    'filepath, expected_extension,returned_filepath',
    [  # String paths
        ('some_filename', '.ext', 'some_filename.ext'),  # filename w/o ext
        pytest.param('some_filename', '.ext', 'some_filename',
                     marks=pytest.mark.xfail(reason="Correct ext no appended.")),
        ('some_filename.ext', '.ext', 'some_filename.ext'),  # filename w/correct ext
        pytest.param('some_filename.ext', '.ext', 'some_filename.ext.ext',
                     marks=pytest.mark.xfail(reason="If path: duplicate correct ext added.")),
        ('some_filename.other_ext', '.ext', 'some_filename.other_ext.ext'),  # filename w/wrong ext
        pytest.param('some_filename.other_ext', '.ext', 'some_filename.other_ext',
                     marks=pytest.mark.xfail(reason="If pass: correct ext not added.")),
        pytest.param('some_filename.other_ext', '.ext', 'some_filename.ext',
                     marks=pytest.mark.xfail(reason="If pass: wrong ext no preserved.")),
        ('some_filename.an_ext.other_ext', '.ext', 'some_filename.an_ext.other_ext.ext'),
        # pathlib.Path paths
        (Path('some_filename'), '.ext', Path('some_filename.ext')),  # filename w/o ext
        pytest.param(Path('some_filename'), '.ext', Path('some_filename'),
                     marks=pytest.mark.xfail(reason="Correct ext no appended.")),
        (Path('some_filename.ext'), '.ext', Path('some_filename.ext')),  # filename w/correct ext
        pytest.param(Path('some_filename.ext'), '.ext', Path('some_filename.ext.ext'),
                     marks=pytest.mark.xfail(reason="If path: duplicate correct ext added.")),
        (Path('some_filename.other_ext'), '.ext', Path('some_filename.other_ext.ext')),  # filename w/wrong ext
        pytest.param(Path('some_filename.other_ext'), '.ext', Path('some_filename.other_ext'),
                     marks=pytest.mark.xfail(reason="If pass: correct ext not added.")),
        pytest.param(Path('some_filename.other_ext'), '.ext', Path('some_filename.ext'),
                     marks=pytest.mark.xfail(reason="If pass: wrong ext no preserved.")),
        (Path('some_filename.an_ext.other_ext'), '.ext', Path('some_filename.an_ext.other_ext.ext')),
        (Path('some_filename.an_ext.other_ext.yet_another_ext.wow_many_exts'), '.ext', Path('some_filename.an_ext.other_ext.yet_another_ext.wow_many_exts.ext')),
    ])
def test_ensure_extension(filepath, expected_extension, returned_filepath):
    assert ensure_extension(filepath, expected_extension) == returned_filepath
