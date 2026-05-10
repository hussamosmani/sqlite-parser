from typing import Optional

from app.command_processor.tables_command_processor import TablesCommandProcessor
from app.command_processor.db_info_command_processor import DbInfoCommandProcessor
from app.command_processor.select_command_processor import SelectCommandProcessor
from app.argument_parser.argument_parser_interface import Command

from .argument_processor_interface import ArgumentProcessorInterface

class ArgumentProcessor(ArgumentProcessorInterface):
    
    def __init__(self,db_info_command_processor: DbInfoCommandProcessor,
                  tables_command_processor: TablesCommandProcessor,
                  select_command_processor: SelectCommandProcessor) -> None:
        self._db_info_command_processor = db_info_command_processor
        self._tables_command_processor = tables_command_processor
        self._select_command_processor = select_command_processor

    def process_argument(self, command: Command, sql: str):
        if command == Command.DB_INFO:
            self._db_info_command_processor.process()
        elif command == Command.TABLES:
            self._tables_command_processor.process()
        elif command == Command.SELECT:
            assert sql is not None
            self._select_command_processor.process(sql)
    
    def _process_argument_of_type_tables(self):
        pass