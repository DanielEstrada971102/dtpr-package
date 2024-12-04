""" Miscelaneous """

import math


_noDelete = {"lines": []}


def color_msg(msg, color="none", indentLevel=-1, return_str=False):
    """
    Prints a message with ANSI coding so it can be printed with colors.

    Args:
        msg (str): The message to print.
        color (str): The color to use for the message. Default is "none".
        indentLevel (int): The level of indentation. Default is -1.
        return_str (bool): If True, returns the formatted message as a string. Default is False.

    Returns:
        str: The formatted message if return_str is True.
    """
    codes = {
        "none": "0m",
        "green": "1;32m",
        "red": "1;31m",
        "blue": "1;34m",
        "yellow": "1;33m",
        "purple": "1;35m",
    }

    indentStr = ""
    if indentLevel == 0:
        indentStr = ">>"
    if indentLevel == 1:
        indentStr = "+"
    if indentLevel == 2:
        indentStr = "*"
    if indentLevel == 3:
        indentStr = "-->"
    if indentLevel >= 4:
        indentStr = "-"

    try:
        formatted_msg = "\033[%s%s %s \033[0m" % (
            codes[color],
            "  " * indentLevel + indentStr,
            msg,
        )
    except KeyError:
        formatted_msg = "\033[%s%s %s \033[0m" % (
            codes["none"],
            "  " * indentLevel + indentStr,
            msg,
        )

    if return_str:
        return formatted_msg
    else:
        print(formatted_msg)


def warning_handler(message, category, filename, lineno, file=None, line=None):
    """
    Handles warnings by printing them with color formatting.

    Args:
        message (str): The warning message.
        category (Warning): The category of the warning.
        filename (str): The name of the file where the warning occurred.
        lineno (int): The line number where the warning occurred.
        file (file object, optional): The file object. Default is None.
        line (str, optional): The line of code where the warning occurred. Default is None.
    """
    print(
        "".join(
            [
                color_msg(
                    f"{category.__name__} in:",
                    color="yellow",
                    return_str=True,
                    indentLevel=-1,
                ),
                color_msg(
                    f"{filename}-{lineno} :",
                    color="purple",
                    return_str=True,
                    indentLevel=-1,
                ),
                color_msg(f"{message}", return_str=True, indentLevel=-1),
            ]
        )
    )


def error_handler(exc_type, exc_value, exc_traceback):
    """
    Handles errors by printing them with color formatting.

    Args:
        exc_type (type): The type of the exception.
        exc_value (Exception): The exception instance.
        exc_traceback (traceback): The traceback object.
    """
    import traceback

    print(
        "".join(
            [
                color_msg(
                    f"{exc_type.__name__}:",
                    color="red",
                    return_str=True,
                    indentLevel=-1,
                ),
                color_msg(
                    f"{exc_value}", color="yellow", return_str=True, indentLevel=-1
                ),
                color_msg(
                    (
                        "Traceback (most recent call last):"
                        + "".join(traceback.format_tb(exc_traceback))
                        if exc_traceback
                        else ""
                    ),
                    return_str=True,
                    indentLevel=-1,
                ),  # [-2:]
            ]
        )
    )

def deltaPhi(phi1, phi2):
    """
    Calculates the difference in phi between two angles.

    Args:
        phi1 (float): The first angle in radians.
        phi2 (float): The second angle in radians.

    Returns:
        float: The difference in phi.
    """
    res = phi1 - phi2
    while res > math.pi:
        res -= 2 * math.pi
    while res <= -math.pi:
        res += 2 * math.pi
    return res


def deltaR(p1, p2):
    """
    Calculates the delta R between two particles.

    Args:
        p1 (object): The first particle with attributes eta and phi.
        p2 (object): The second particle with attributes eta and phi.

    Returns:
        float: The delta R value.
    """
    dEta = abs(p1.eta - p2.eta)
    dPhi = deltaPhi(p1.phi, p2.phi)
    return math.sqrt(dEta * dEta + dPhi * dPhi)


def phiConv(phi):
    """
    Converts a phi value.

    Args:
        phi (float): The phi value to convert.

    Returns:
        float: The converted phi value.
    """
    return 0.5 * phi / 65536.0

