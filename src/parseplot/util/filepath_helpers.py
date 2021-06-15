"""Helper methods for dealing with files and paths."""
from pathlib import Path
from typing import Union


def ensure_extension(filepath: Union[str, Path], extension: str) -> Union[str, Path]:
    """
    Adds given extension to a given filepath, if necessary.

    Preserves any previously existent extensions, appending desired extension.

    :param filepath: Union[str, Path])
    :param extension: str
    :return: Union[str, Path])
    """
    if isinstance(filepath, Path):
        if filepath.suffix != extension:
            if filepath.suffix:
                extension = filepath.suffix + extension  # Preserve existing suffix.
            filepath = filepath.with_suffix(extension)
    elif not filepath.endswith(extension):  # Path does not have .endswith
        filepath += extension
    return filepath
