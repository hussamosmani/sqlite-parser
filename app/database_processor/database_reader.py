from typing import Tuple


class DatabaseReader:
    PAGE_SIZE_OFFSET = 16
    NUMBER_OF_CELLS_OFFSET = 103
    END_OF_DB_HEADER = 108

    def __init__(self,database_file_path: str):
        self._database_file = open(database_file_path, "rb")

    
    def retrieve_bytes_at_offset(self, offset:int, byte_size: int) -> bytes:
        self._database_file.seek(offset)
        return self._database_file.read(byte_size)
    
    def retrieve_bytes_at_offset_as_int(self, offset: int, byte_size: int,) -> int:
        data = self.retrieve_bytes_at_offset(offset,byte_size)
        return int.from_bytes(data, byteorder="big")

    def read_var_int_starting_at_offset(self, offset: int) -> Tuple[int, int]:
        is_continuation_bit_zero = False
        bytes_to_concatenate = []
        while not is_continuation_bit_zero:
            byte_to_decode = self.retrieve_bytes_at_offset_as_int(offset,1)
            byte_to_decode_shifted = byte_to_decode >> 7
            byte_to_decode_continuation_bit = byte_to_decode_shifted & 0x0000001
            is_continuation_bit_zero = byte_to_decode_continuation_bit == 0
            bytes_to_decode_payload = byte_to_decode & 0b01111111
            bytes_to_concatenate.append(format(bytes_to_decode_payload, "07b"))
            offset += 1
        
        big_endian2s_complement_decoded_string = "".join(bytes_to_concatenate)
        return int(big_endian2s_complement_decoded_string, 2), offset
    
    def close(self):
        self._database_file.close()