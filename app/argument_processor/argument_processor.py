from typing import Optional

from command_processor.tables_command_processor import TablesCommandProcessor
from command_processor.db_info_command_processor import DbInfoCommandProcessor
from argument_parser.argument_parser_interface import Command

from .argument_processor_interface import ArgumentProcessorInterface
from argument_parser.argument_parser import ArgumentParser

class ArgumentProcessor(ArgumentProcessorInterface):
    
    def __init__(self,db_info_command_processor: DbInfoCommandProcessor, tables_command_processor: TablesCommandProcessor) -> None:
        self._db_info_command_processor = db_info_command_processor
        self._tables_command_processor = tables_command_processor

    def process_argument(self, command: Command, sql: Optional[str]):
        if command == Command.DB_INFO:
            self._db_info_command_processor.process()
        elif command == Command.TABLES:
            self._tables_command_processor.process()
        elif command == Command.SELECT:
            pass
    
    def _process_argument_of_type_tables(self):
        pass