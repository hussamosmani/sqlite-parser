from dataclasses import dataclass
from typing import Optional

from app.database_processor.database_reader import DatabaseReader


@dataclass
class RecordHeader:
    header_size: Optional[int]
    record_type_size: Optional[int]
    record_name_size: Optional[int]
    table_name_size: Optional[int]
    rootpage_size: Optional[int]
    sql_size: Optional[int]
    body_offset: Optional[int]


class DatabaseRecordProcessor:
    def __init__(self, database_reader: DatabaseReader) -> None:
        self._database_reader = database_reader

    def parse_header(self, offset: int) -> RecordHeader:
        size_of_record, offset_of_record_id = (
            self._database_reader.read_var_int_starting_at_offset(offset)
        )

        record_id_at_offset, offset_of_record_header = (
            self._database_reader.read_var_int_starting_at_offset(offset_of_record_id)
        )

        size_of_record_header, offset_of_record_sqlite_schema_type = (
            self._database_reader.read_var_int_starting_at_offset(offset_of_record_header)
        )

        size_of_record_type, offset_of_record_sqlite_schema_name = (
            self._database_reader.read_var_int_starting_at_offset(offset_of_record_sqlite_schema_type)
        )

        size_of_record_name, offset_of_record_sqlite_schema_table_name = (
            self._database_reader.read_var_int_starting_at_offset(offset_of_record_sqlite_schema_name)
        )

        size_of_record_table_name, offset_of_record_sqlite_rootpage = (
            self._database_reader.read_var_int_starting_at_offset(offset_of_record_sqlite_schema_table_name)
        )

        size_of_record_rootpage, offset_of_record_sqlite_sql = (
            self._database_reader.read_var_int_starting_at_offset(offset_of_record_sqlite_rootpage)
        )

        size_of_record_sql, offset_of_record_body = (
            self._database_reader.read_var_int_starting_at_offset(offset_of_record_sqlite_sql)
        )

        return RecordHeader(
            header_size=self._serial_type_to_size(size_of_record_header),
            record_type_size=self._serial_type_to_size(size_of_record_type),
            record_name_size=self._serial_type_to_size(size_of_record_name),
            table_name_size=self._serial_type_to_size(size_of_record_table_name),
            rootpage_size=self._serial_type_to_size(size_of_record_rootpage),
            sql_size=self._serial_type_to_size(size_of_record_sql),
            body_offset=offset_of_record_body,
        )
    
    def get_root_page_from_record_header(self,record_header: RecordHeader) -> int:
        assert record_header.body_offset is not None
        assert record_header.record_type_size is not None
        assert record_header.record_name_size is not None
        assert record_header.table_name_size is not None
        assert record_header.rootpage_size is not None
        
        offset_to_root_page = record_header.body_offset + record_header.record_type_size + record_header.record_name_size + record_header.table_name_size
        return self._database_reader.retrieve_bytes_at_offset_as_int(offset_to_root_page, record_header.rootpage_size)
    
    def get_table_name_from_record_header(self, record_header: RecordHeader) -> str:
        assert record_header.body_offset is not None
        assert record_header.record_type_size is not None
        assert record_header.record_name_size is not None
        assert record_header.table_name_size is not None
        offset_to_table_name_in_record = record_header.body_offset + record_header.record_type_size + record_header.record_name_size
        table_name_as_bytes = self._database_reader.retrieve_bytes_at_offset(offset_to_table_name_in_record, record_header.table_name_size)
        return table_name_as_bytes.decode("utf-8")


    def _serial_type_to_size(self, serial_type: int) -> Optional[int]:
        if serial_type == 0:
            return 0
        elif serial_type == 1:
            return 1
        elif serial_type == 2:
            return 2
        elif serial_type == 3:
            return 3
        elif serial_type == 4:
            return 4
        elif serial_type == 5:
            return 6
        elif serial_type == 6:
            return 8
        elif serial_type == 7:
            return 8
        elif serial_type == 8:
            return 0
        elif serial_type == 9:
            return 0
        elif serial_type in (10, 11):
            return None
        elif serial_type >= 12:
            if serial_type % 2 == 0:
                return (serial_type - 12) // 2
            return (serial_type - 13) // 2

        return None