from typing import List

from app.database_processor.database_reader import DatabaseReader


class DatabaseSchemaProcessor:
    PAGE_SIZE_OFFSET = 16
    NUMBER_OF_CELLS_OFFSET = 103
    END_OF_DB_HEADER = 108

    def __init__(self,database_reader: DatabaseReader):
        self._database_reader = database_reader

    def get_page_size(self):
        return self._database_reader.retrieve_bytes_at_offset_as_int(self.PAGE_SIZE_OFFSET, 2)
    
    def get_number_of_tables(self, offset = NUMBER_OF_CELLS_OFFSET ):
        return self._database_reader.retrieve_bytes_at_offset_as_int(offset,2)
    
    def get_cell_pointer_array_offsets(self) -> List[int]:
        number_of_cells = self.get_number_of_tables()
        cell_content_offsets_array = []
        sizeof_cell_pointer_in_bytes = 2
        for k in range(0, number_of_cells):
            offset_to_kth_cell_pointer_array_entry = self.END_OF_DB_HEADER + k * sizeof_cell_pointer_in_bytes
            offset_to_kth_cell_pointer = self._database_reader.retrieve_bytes_at_offset_as_int(offset_to_kth_cell_pointer_array_entry,2)
            cell_content_offsets_array.append(offset_to_kth_cell_pointer)
        return cell_content_offsets_array