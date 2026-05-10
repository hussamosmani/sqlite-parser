from abc import ABC,abstractmethod
from enum import Enum

class Command(Enum):
    TABLES = 1
    DB_INFO = 2
    SELECT = 3
    NOT_SUPPORTED = 4

# Interface for parsing arguments entered by user.
class ArgumentParserInterface(ABC):

    @abstractmethod
    def parse_command(self,command: str) -> Command:
        pass