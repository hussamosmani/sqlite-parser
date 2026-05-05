import sys

from typing import BinaryIO, List, Tuple

database_file_path = sys.argv[1]
command = sys.argv[2]
end_of_db_header = 108
cell_pointer_entry_size_in_bytes = 2

def read_database_file(database_file: BinaryIO, byte_size: int) -> int:
    return int.from_bytes(database_file.read(byte_size), byteorder="big")

def read_database_file_as_bytes(database_file: BinaryIO, byte_size: int) -> bytes:
    return database_file.read(byte_size)

def get_number_of_cells(database_file: BinaryIO) -> int:
    database_file.seek(103)
    number_of_cells = read_database_file(database_file=database_file, byte_size=2)
    return number_of_cells

def get_cell_pointer_array_offsets(database_file: BinaryIO, number_of_cells: int) -> List[int]:
    cell_content_offsets_array = []
    for k in range(0, number_of_cells):
        cell_pointer_array_two_byte_offset_to_cell_content = end_of_db_header + k * cell_pointer_entry_size_in_bytes
        database_file.seek(cell_pointer_array_two_byte_offset_to_cell_content)
        cell_content_offset_for_kth_cell = read_database_file(database_file=database_file, byte_size=2)
        cell_content_offsets_array.append(cell_content_offset_for_kth_cell)
    return cell_content_offsets_array

def read_var_int_starting_at_offset(database_file: BinaryIO, offset: int) -> Tuple[int, int]:
    is_continuation_bit_zero = False
    bytes_to_concatenate = []
    while not is_continuation_bit_zero:
        database_file.seek(offset)
        byte_to_decode = read_database_file(database_file=database_file, byte_size=1)
        byte_to_decode_shifted = byte_to_decode >> 7
        byte_to_decode_continuation_bit = byte_to_decode_shifted & 0x0000001
        is_continuation_bit_zero = byte_to_decode_continuation_bit == 0
        bytes_to_decode_payload = byte_to_decode & 0b01111111
        bytes_to_concatenate.append(format(bytes_to_decode_payload, "07b"))
        offset += 1
    
    big_endian2s_complement_decoded_string = "".join(bytes_to_concatenate)
    return int(big_endian2s_complement_decoded_string, 2), offset

def serial_type_to_content_type(serial_type: int):
    if serial_type == 0:
        return ("null", 0)

    elif serial_type == 1:
        return ("int8", 1)

    elif serial_type == 2:
        return ("int16", 2)

    elif serial_type == 3:
        return ("int24", 3)

    elif serial_type == 4:
        return ("int32", 4)

    elif serial_type == 5:
        return ("int48", 6)

    elif serial_type == 6:
        return ("int64", 8)

    elif serial_type == 7:
        return ("float64", 8)

    elif serial_type == 8:
        return ("int", 0)  # value = 0

    elif serial_type == 9:
        return ("int", 0)  # value = 1

    elif serial_type in (10, 11):
        return ("reserved", None)

    elif serial_type >= 12:
        if serial_type % 2 == 0:
            size = (serial_type - 12) // 2
            return ("blob", size)
        else:
            size = (serial_type - 13) // 2
            return ("text", size)

def parse_record_header_at_offset(database_file: BinaryIO, offset: int):
    size_of_record_header, offset_of_record_sql_lite_schema_type = read_var_int_starting_at_offset(database_file=database_file, offset=offset)
    size_of_record_type, offset_of_record_sql_lite_schema_name = read_var_int_starting_at_offset(database_file=database_file, offset=offset_of_record_sql_lite_schema_type)
    size_of_record_name, offset_of_record_sql_lite_schema_table_name = read_var_int_starting_at_offset(database_file=database_file, offset=offset_of_record_sql_lite_schema_name)
    size_of_record_table_name, offset_of_record_sql_lite_rootpage = read_var_int_starting_at_offset(database_file=database_file, offset=offset_of_record_sql_lite_schema_table_name)
    size_of_record_rootpage, offset_of_record_sql_lite_sql = read_var_int_starting_at_offset(database_file=database_file, offset=offset_of_record_sql_lite_rootpage)
    size_of_record_sql, offset_of_record_body = read_var_int_starting_at_offset(database_file=database_file, offset=offset_of_record_sql_lite_sql)

    return [
        serial_type_to_content_type(size_of_record_header),
        serial_type_to_content_type(size_of_record_type),
        serial_type_to_content_type(size_of_record_name),
        serial_type_to_content_type(size_of_record_table_name),
        serial_type_to_content_type(size_of_record_rootpage),
        serial_type_to_content_type(size_of_record_sql)
    ], offset_of_record_body

if command == ".dbinfo":
    with open(database_file_path, "rb") as database_file:
        print("Logs from your program will appear here!", file=sys.stderr)

        database_file.seek(16)
        page_size = int.from_bytes(database_file.read(2), byteorder="big")
        print(f"database page size: {page_size}")

        print(f"number of tables: {get_number_of_cells(database_file=database_file)}")

if command == ".tables":
    with open(database_file_path, "rb") as database_file:
        number_of_cells = get_number_of_cells(database_file=database_file)
        cell_content_offsets_array = get_cell_pointer_array_offsets(
            database_file=database_file,
            number_of_cells=number_of_cells
        )

        for cell_content_offset in cell_content_offsets_array:
            size_of_record_at_offset, offset_of_record_id = read_var_int_starting_at_offset(
                database_file=database_file,
                offset=cell_content_offset
            )

            record_id_at_offset, offset_of_record_header = read_var_int_starting_at_offset(
                database_file=database_file,
                offset=offset_of_record_id
            )

            header_fields, offset_of_record_body = parse_record_header_at_offset(
                database_file=database_file,
                offset=offset_of_record_header
            )

            record_header, record_type, record_name, record_table_name, record_rootpage, record_sql = header_fields

            record_header_type, record_header_size = record_header
            record_type_type, record_type_size = record_type
            record_name_type, record_name_size = record_name
            record_table_name_type, record_table_name_size = record_table_name
            record_rootpage_type, record_rootpage_size = record_rootpage
            record_sql_type, record_sql_size = record_sql

            database_file.seek(offset_of_record_body + record_type_size + record_name_size)

            table_name = read_database_file_as_bytes(
                database_file=database_file,
                byte_size=record_table_name_size
            ).decode("utf-8")

            if table_name != "sqlite_sequence":
                print(table_name)