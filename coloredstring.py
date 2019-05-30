"""The ColoredString class (provided as `cs` for ease-of-use) is
used to generate strings that will be printed with colors in a
terminal that supports ANSI color codes. The color highlighting
syntax is as follows:

Using a marker, you can specify where you want to start coloring
in the text. A marker is denoted by a caret symbol (^) followed
by a color ID. Optionally, you can append a repeater, in the
format of '*[1, 2, 3, ...]' to specify how many characters should
be highlighted by the marker that precedes it.

                Color IDs
        --------------------------
Color   Foreground      Background
-----   ----------      ----------
white       0               a
green       1               b
red         2               c
yellow      3               d
blue        4               e
cyan        5               f
white       6               g
magenta     7               h
black       8               i

Other color IDs include:

Color ID    Use
--------    ---
.           Set to default foreground
,           Set to default background
:           Set to default foreground & background
~           Set to complement of foreground & background

Examples:

    ^1Hello             prints "Hello" in green
    ^1H^aello           prints "H" in green and "ello" in the default color with a white background
    ^5*3Hello           prints "Hel" in cyan and the rest with the default color
    ^1Hello ^:world     prints "Hello " in green and resets it so that "world" prints with the default foreground
"""

import re

from typing import Tuple, Match

class UnsafeRepeaterException(Exception):
    """Used to let the user know that a repeater with a bad
    count value was specified. Running that repeater against
    the ColoredString class would likely cause it to crash.
    """
    def __init__(self, count) -> None:
        """Initializes an UnsafeRepeaterException by storing the
        count value that caused a red flag."""
        super().__init__("Unsafe repeater was specified (out-of-bounds)")

        self.count = count

class ColoredString:
    """Specify a string using the syntax stated above and this
    class will be able to convert the string into an ANSI color
    coded string with the use of the __str__ method.
    """
    # Regular expressions / patterns
    _color_pattern = r'\^[a-i0-8]'
    _repeater_pattern = r'[*]+[1-9]+'
    _color_and_repeater_pattern = ''.join([_color_pattern, _repeater_pattern])
    _color_or_repeater_pattern = '|'.join([_color_pattern, _repeater_pattern])

    # Compiled regular expressions
    _color_regexp = re.compile(_color_pattern)
    _repeater_regexp = re.compile(_repeater_pattern)
    _color_and_repeater_regexp = re.compile(_color_and_repeater_pattern)
    _color_or_repeater_regexp = re.compile(_color_or_repeater_pattern)

    def __init__(self, string: str) -> None:
        """Initialize an instance of ColoredString."""
        self.string = string

    def __str__(self) -> str:
        """Converts self.string from our syntax into an ANSI
        colored coded string ready for printing to the terminal.
        """
        return self.process(self.string)

    def process(self, string: str) -> str:
        """Process self.string by applying the following rules
        and returns an ANSI color code compliant string:

            1. Check all instances of repeaters for safety (not out-of-bounds)
            2. Replace all instances of repeaters with the ANSI color reset code
            3. Replace all instances of color specifiers with their ANSI color codes
        """
        self._check_all_repeaters(string)
        no_repeaters_str = self._process_repeaters(string)
        ansi_compliant_str = self._process_colors(no_repeaters_str)

        return ansi_compliant_str

    def _check_all_repeaters(self, string: str) -> None:
        """Iterates through all the repeaters in the string of the
        format *[count] where count = 1, 2, 3, etc. and ensures that
        there are no count values that are out-of-bound.
        """
        for match in self._color_and_repeater_regexp.finditer(string):
            unsafe_check_info = self._is_unsafe_repeater(match)
            if unsafe_check_info[0]:
                raise UnsafeRepeaterException(unsafe_check_info[1])

    def _is_unsafe_repeater(self, match: Match) -> Tuple[bool, int]:
        """Determines whether the matched repeater is a safe repeater
        by checking whether the count index is out-of-bounds.
        """

        # Calculate the maximum number that can be specified by the repeater
        # in this instance by looking ahead at the characters left.
        str_after_match = match.string[match.start() + len(match.group()):]
        remaining_chars_len = self._remaining_str_len(str_after_match)

        repeater_count_str = re.search('\*([1-9]+)', match.group()).groups()[0]
        repeater_count = int(repeater_count_str)

        if repeater_count > remaining_chars_len:
            return True, repeater_count

        return False, -1

    def _process_repeaters(self, string: str) -> str:
        """Replaces all instances of repeaters with an ANSI color
        reset code at the 'count' position specified by the repeater.
        """
        return string # TODO: Placeholder, change!

    def _process_colors(self, string: str) -> str:
        """Replaces all instances of color specifiers in the format
        of ^[color] with the ANSI color equivalent.
        """
        return string # TODO: Placeholder, change!

    def _remaining_str_len(self, s: str) -> int:
        """Calculates the number of characters left for use with the
        repeater specifier by ignoring color or repeater specifiers
        as those will be stripped out during processing."""
        total_remaining_chars = len(s) # includes color/repeater specifiers

        specifiers_used = ''.join(self._color_or_repeater_regexp.findall(s))
        specifier_chars_len = len(specifiers_used) # length of specifier strings used

        return total_remaining_chars - specifier_chars_len


# Provided for ease-of-typing.
cs = ColoredString