"""The `fs` class is used to generate a Linux-style string that uses
colors from the syntax that colorformat uses. To identify where you
want colors to be highlighted, use the following syntax:

Use a marker to start highlighting the characters from the position
onwards. A marker is denoted by a ^ symbol followed by color IDs and
a "count specifier" at the end signified by *[1, 2 , 3].

Color IDs (foreground):
    0 -> white
    1 -> green
    2 -> red
    3 -> yellow
    4 -> blue
    5 -> cyan
    6 -> white
    7 -> magenta
    8 -> black

Color IDs (background):
    a -> white
    b -> green
    c -> red
    d -> yellow
    e -> blue
    f -> cyan
    g -> white
    h -> magenta
    i -> black

Color IDs (other):
    . -> default foreground
    , -> default background
    : -> default foreground and background
    ~ -> complement of foreground and background

Examples:

    ^1Hello             prints the string "Hello" in green
    ^1H^2ello           prints "H" in green, "ello" in red
    ^1Hello ^.world     prints "Hello" in green, "world" in the default foreground color
    ^b*2Hello           prints "He" with a green background, "llo" with the default background color

"""

# NOTE: Use re.compile to generate a regular expression object and store it rather than
# using re.match(a, b) every time to create a new object. Store it as a global.


import re

from typing import Match, List

# TODO: Fix these names.

# Pattern used to identify repeaters.
COLOR_PATTERN = r'\^[a-i0-8]'
REPEATER_PATTERN = r'\^[a-i0-8][*]+[1-9]+'
REPEATER_ONLY_PATTERN = r'[*]+[1-9]+'
COLOR_OR_REPEATER_PATTERN = r'|'.join([REPEATER_PATTERN, COLOR_PATTERN])

# Compile regular expressions
COLOR_REGEXP = re.compile(COLOR_PATTERN)
REPEATER_REGEXP = re.compile(REPEATER_PATTERN)
REPEATER_ONLY_REGEXP = re.compile(REPEATER_ONLY_PATTERN)
COLOR_OR_REPEATER_REGEXP = re.compile(COLOR_OR_REPEATER_PATTERN)

class UnsafeRepeaterException(Exception):
    """Thrown when a bad repeater specifier is found."""
    def __init__(self):
        super().__init__("Unsafe repeater, bad counter specifier found")

class FormatString:
    def __init__(self, string: str) -> None:
        """Initialize format string object with syntax riddled string."""
        self.string = string

    def __str__(self) -> str:
        """Converts the stored string with the ANSI color coded equivalent."""
        self.__process_string()

        # TODO: Replace this
        return self.string

    def __process_string(self) -> str:
        """Processes the stored string by iterating over the characters from
        left to right and replacing our syntax with the appropriate ANSI
        color codes in the right positions.
        """
        self.__replace_repeaters()

    def __is_unsafe_repeater(self, match: Match) -> bool:
        """A repeater may be unsafe if it specifies a count value that goes
        over the length of the provided string."""


        # Count the number of characters in the remaining part of the string
        # that don't match any of the regexps that we have.

        # Get the remaining string after the matched regex.
        match_found_pos = match.start()
        matched_pattern = match.group()
        str_after_match = match.string[match_found_pos + len(matched_pattern):]

        # Find the max value of the repeater count specifier by finding the
        # length of the remaining string without our patterns in them.
        total_str_len = len(str_after_match)
        all_patterns_used = ''.join(COLOR_OR_REPEATER_REGEXP.findall(str_after_match))
        other_matches_len = len(all_patterns_used)

        # We calculate the max length. TODO: Document this!
        pattern_stripped_str_len = len(str_after_match) - other_matches_len - 1

        repeater_counter = int(match.group().split('*')[1])
        if repeater_counter > pattern_stripped_str_len:
            return True

        return False

    def __get_insert_pos(self, match: Match) -> int:
        matched_pattern = match.group()
        resetter_pos = int(matched_pattern.split('*')[1])

        # Insert the reset code at the relative position specified.
        match_end_pos = match.end()
        reset_insert_pos = match_end_pos + resetter_pos

        return reset_insert_pos

    def __insert_resetters(self, positions: List[str]) -> None:
        """Inserts the reset ANSI color codes at the specified positions."""
        # Find all the instances of the repeater and insert a resetter
        # at the position required.
        for p in positions:
            # TODO: Replace with class that manages colors
            self.string = self.string[:p] + '\u001b[0m' + self.string[p:]

    def __clear_repeaters(self) -> None:
        """Remove all instances of a repeater."""
        self.string = REPEATER_ONLY_REGEXP.sub('', self.string)

    def __replace_repeaters(self) -> None:
        """Replaces all instances of *[count] in ^[colorid]*[count] with a
        reset string `count` characters down the string."""

        # Check whether the provided string complies to our specifications
        # then collect all the positions to insert a ANSI reset color code.
        insert_positions = []
        for m in REPEATER_REGEXP.finditer(self.string):
            if self.__is_unsafe_repeater(m):
                raise UnsafeRepeaterException()
            insert_positions.append(self.__get_insert_pos(m))
        self.__insert_resetters(insert_positions)
        self.__clear_repeaters()


fs = FormatString    # Ease-of-typing

# Regex
#
# *1, *2, *3, .. => *[number from 1-remaining string length]
# *digit*
# *[0-9]+
#
# ^1*2Hello = 5=max, 1=min,

#print(fs("^1*1Hello ^2*5world!"))