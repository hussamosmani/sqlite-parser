import sys

from dataclasses import dataclass

# import sqlparse - available if you need it!

database_file_path = sys.argv[1]
command = sys.argv[2]

if command == ".dbinfo":
    with open(database_file_path, "rb") as database_file:
        # You can use print statements as follows for debugging, they'll be visible when running tests.
        print("Logs from your program will appear here!", file=sys.stderr)

        # Uncomment this to pass the first stage
        database_file.seek(16)
        page_size = int.from_bytes(database_file.read(2), byteorder="big")
        print(f"database page size: {page_size}")

        database_file.seek(28)
        numbero_of_tables = int.from_bytes(database_file.read(4), byteorder="big")
        print(f"number of tables: {numbero_of_tables}")
else:
    print(f"Invalid command: {command}")
