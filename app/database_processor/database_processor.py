from typing import List

from database_processor.database_record_processor import DatabaseRecordProcessor
from database_processor.database_schema_processor import DatabaseSchemaProcessor
from database_processor.database_reader import DatabaseReader


class DatabaseProcessor:

    def __init__(self,database_schema_processor: DatabaseSchemaProcessor, database_record_processor: DatabaseRecordProcessor):
        self._database_schema_processor = database_schema_processor
        self._database_record_processor = database_record_processor
    
    def get_page_size(self):
        return self._database_schema_processor.get_page_size()
    
    def get_number_of_tables(self):
        return self._database_schema_processor.get_number_of_tables()
    
    def get_table_name_from_record_at_offset(self,offset:int) -> str:
        record_header = self._database_record_processor.parse_header(offset)
        return self._database_record_processor.get_table_name_from_record_header(record_header)
    
    def get_cell_pointer_array_offsets(self) -> List[int]:
        return self._database_schema_processor.get_cell_pointer_array_offsets()