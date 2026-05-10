from app.database_processor.database_processor import DatabaseProcessor


class TablesCommandProcessor:
    SQLITE_TABLE_NAME = "sqlite_sequence"
    def __init__(self, database_processor: DatabaseProcessor) -> None:
        self._database_processor = database_processor

    def process(self):
        cell_pointer_array_offsets = self._database_processor.get_cell_pointer_array_offsets()

        for offset in cell_pointer_array_offsets:
            table_name = self._database_processor.get_table_name_from_record_at_offset(offset)
            if table_name != self.SQLITE_TABLE_NAME:
                print(table_name)
