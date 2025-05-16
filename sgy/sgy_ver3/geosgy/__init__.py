from .segy import SEGY

from .reader.reader import Reader
from .parser.parser import Parser
from .modifier.modifier import Modifier

__version__ = "0.0.3"

__all__ = [
    "SEGY",
    "Reader",
    "Parser",
    "Modifier"
]