"""Pre parse string cleansing"""


def pre_parse_translate(initial_string: str) -> str:
    """
    Takes unparsable syntax and replaces with parser-accepted equivalent

    ^ for superscript translated to **


    :param initial_string: str
    :return: str
    """
    clean_string = initial_string.replace("^", "**")

    return clean_string
