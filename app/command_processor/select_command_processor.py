from app.database_processor.database_processor import DatabaseProcessor


class SelectCommandProcessor:
        
    COUNT_ALL_KEYWORDS = "COUNT(*)"

    def __init__(self, database_processor: DatabaseProcessor) -> None:
        self._database_processor = database_processor
    
    def process(self, sql: str):
        select_keyword, select_expression, from_keyword, table_name = sql.split(" ")

        target_record_offset = self._get_offset_to_target_record(table_name)
        root_page = self._database_processor.get_root_page_from_record_at_offset(target_record_offset)
        offset_to_root_page = (root_page - 1) * self._database_processor.get_page_size()  
        count_in_leaf_page = self._database_processor.get_number_of_tables(offset_to_root_page)
        print(count_in_leaf_page)

    def _get_offset_to_target_record(self, table_name: str):
        target_record_offset = None
        cell_pointer_array_offsets = self._database_processor.get_cell_pointer_array_offsets()

        for offset in cell_pointer_array_offsets:
            table_name_at_offset = self._database_processor.get_table_name_from_record_at_offset(offset)
            if table_name == table_name_at_offset:
                target_record_offset = offset
        assert target_record_offset is not None
        return target_record_offset