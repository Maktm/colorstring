import abc
import re

from typing import Optional
from collections import deque

cspattern = re.compile(r'\^\[([a-zA-Z0-9.,:]+)\]')

class Processor(abc.ABC):
    @abc.abstractmethod
    def process(self, s: str) -> str:
        pass

class ResetProcessor(Processor):
    def process(self, s: str) -> Optional[str]:
        ansi_codes = []
        for m in re.finditer(r'[.,:]', s):
            ansi_codes.append({
                '.': '39',
                ',': '49',
                ':': '0'
            }[m.group()])

        if len(ansi_codes) == 0:
            return None

        return ';'.join(ansi_codes)

class EffectsProcessor(Processor):
    def process(self, s: str) -> Optional[str]:
        ansi_codes = []
        for m in re.finditer(r'[nBuyStio]', s):
            ansi_codes.append({
                'n': '22',
                'B': '1',
                'u': '4',
                'y': '24',
                'S': '9',
                't': '29',
                'i': '3',
                'o': '23'
            }[m.group()])

        if len(ansi_codes) == 0:
            return None

        return ';'.join(ansi_codes)

class FgColorProcessor(Processor):
    def process(self, s: str) -> Optional[str]:
        ansi_codes = []
        for m in re.finditer(r'f(\d+)', s):
            fgcolor = m.groups()[0]
            conversion = '38;5;{}'.format(fgcolor)
            ansi_codes.append(conversion)

        if len(ansi_codes) == 0:
            return None

        return ';'.join(ansi_codes)


class BgColorProcessor(Processor):
    def process(self, s: str) -> Optional[str]:
        ansi_codes = []
        for m in re.finditer(r'b(\d+)', s):
            bgcolor = m.groups()[0]
            conversion = '48;5;{}'.format(bgcolor)
            ansi_codes.append(conversion)

        if len(ansi_codes) == 0:
            return None

        return ';'.join(ansi_codes)

processors = (
    ResetProcessor(),
    EffectsProcessor(),
    FgColorProcessor(),
    BgColorProcessor(),
)

def processcs(s: str) -> str:
    ansi_codes = []
    for processor in processors:
        r = processor.process(s)
        if r is not None:
            ansi_codes.append(r)

    return '\033[' + ';'.join(ansi_codes) + 'm'

def cs(s: str) -> str:
    ansi_conversion = []
    for m in cspattern.finditer(s):
        matched_str = m.group()
        ansi_conversion.append(processcs(matched_str))

    conversions = deque(ansi_conversion)

    return cspattern.sub(lambda m: conversions.popleft(), s)