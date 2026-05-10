import sys

from typing import BinaryIO, List, Tuple

from app.database_processor.database_record_processor import DatabaseRecordProcessor
from database_processor.database_schema_processor import DatabaseSchemaProcessor
from command_processor.tables_command_processor import TablesCommandProcessor
from database_processor.database_reader import DatabaseReader
from command_processor.db_info_command_processor import DbInfoCommandProcessor
from database_processor.database_processor import DatabaseProcessor
from argument_parser.argument_parser import ArgumentParser
from argument_processor.argument_processor import ArgumentProcessor

database_file_path = sys.argv[1]
raw_command = sys.argv[2]
command_from_user_input = raw_command.split(" ")[0]
sql_from_user_input = " ".join(raw_command.split(" ")[1:])

def main():
    database_reader = DatabaseReader(database_file_path)
    database_schema_processor = DatabaseSchemaProcessor(database_reader)
    database_record_processor = DatabaseRecordProcessor(database_reader)
    database_processor = DatabaseProcessor(database_schema_processor,database_record_processor)
    database_info_command_processor = DbInfoCommandProcessor(database_processor)
    database_tables_command_processor = TablesCommandProcessor(database_processor)
    argument_processor = ArgumentProcessor(database_info_command_processor,database_tables_command_processor)
    argument_parser = ArgumentParser()
    
    command = argument_parser.parse_command(command_from_user_input)
    argument_processor.process_argument(command,sql_from_user_input)

    database_reader.close()
main()