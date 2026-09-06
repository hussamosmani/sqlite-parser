from typing import List, Optional

from app.database_processor.database_record_processor import DatabaseRecordProcessor
from app.database_processor.database_schema_processor import DatabaseSchemaProcessor
from app.database_processor.database_reader import DatabaseReader


class DatabaseProcessor:

    def __init__(self,database_schema_processor: DatabaseSchemaProcessor, database_record_processor: DatabaseRecordProcessor, database_reader: DatabaseReader):
        self._database_schema_processor = database_schema_processor
        self._database_record_processor = database_record_processor
        self._database_reader = database_reader
    
    def get_page_size(self):
        return self._database_schema_processor.get_page_size()
    
    def get_number_of_tables(self, offset: Optional[int] = None):
        if offset:
            return self._database_schema_processor.get_number_of_tables(offset + 3)
        return self._database_schema_processor.get_number_of_tables()

    
    def get_table_name_from_record_at_offset(self,offset:int) -> str:
        record_header = self._database_record_processor.parse_header(offset)
        return self._database_record_processor.get_table_name_from_record_header(record_header)

    def get_sql_from_record_at_offset(self,offset:int) -> str:
        record_header = self._database_record_processor.parse_header(offset)
        return self._database_record_processor.get_sql_from_record_header(record_header)
    
    def get_cell_pointer_array_offsets(self) -> List[int]:
        return self._database_schema_processor.get_cell_pointer_array_offsets()
    
    def get_root_page_from_record_at_offset(self, offset: int) -> int:
        record_header = self._database_record_processor.parse_header(offset)
        return self._database_record_processor.get_root_page_from_record_header(record_header)

    def get_cell_content_array_from_rootpage_offset(self, rootpage_offset: int, number_of_cells: int, column_names: List[str]):
        PAGE_HEADER_SIZE_IN_BYTES = 8
        cell_pointer_array_index = rootpage_offset + PAGE_HEADER_SIZE_IN_BYTES
        root_page_type = self._get_page_type_from_hader_at_offset(rootpage_offset)
        cell_pointer_offset_array = []
        cell_content_array = []
        for i in range(0,number_of_cells):
            offset_at_i = self._database_reader.retrieve_bytes_at_offset_as_int(cell_pointer_array_index,2)
            cell_pointer_offset_array.append(offset_at_i)
            cell_pointer_array_index+=2
        for offset in cell_pointer_offset_array:
            cell_content_start_at_offset = rootpage_offset + offset
            record_entries_sizes, cell_content_body_offset = self._database_record_processor.parse_header_generic(cell_content_start_at_offset, len(column_names),root_page_type)
            # add it back to the list
            cell_content_at_offset = []
            for record_entries_size in record_entries_sizes:
                cell_content_at_offset.append(self._database_reader.retrieve_bytes_at_offset(cell_content_body_offset,record_entries_size))
                cell_content_body_offset+=record_entries_size
            cell_content_array.append(cell_content_at_offset)
        return cell_content_array

    def _get_page_type_from_hader_at_offset(self, offset: int):
        return self._database_schema_processor.get_page_type_from_header(offset)