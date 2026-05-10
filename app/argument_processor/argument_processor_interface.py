from abc import ABC, abstractmethod
from typing import Optional
from argument_parser.argument_parser_interface import Command

class ArgumentProcessorInterface(ABC):

    @abstractmethod
    def process_argument(self, command: Command,sql: Optional[str]):
        pass