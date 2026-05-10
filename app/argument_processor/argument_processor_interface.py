from abc import ABC, abstractmethod
from app.argument_parser.argument_parser_interface import Command

class ArgumentProcessorInterface(ABC):

    @abstractmethod
    def process_argument(self, command: Command,sql: str):
        pass