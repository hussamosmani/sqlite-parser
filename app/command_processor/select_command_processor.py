from typing import List

from app.database_processor.database_processor import DatabaseProcessor


class SelectCommandProcessor:
    COUNT_ALL_KEYWORDS_UPPER = "COUNT(*)"
    COUNT_ALL_KEYWORDS_LOWER = "count(*)"

    def __init__(self, database_processor: DatabaseProcessor) -> None:
        self._database_processor = database_processor

    def process(self, sql: str) -> None:
        select_expression, table_name = self._parse_select(sql)

        if select_expression in [self.COUNT_ALL_KEYWORDS_UPPER,self.COUNT_ALL_KEYWORDS_LOWER]:
            self._process_count(table_name)
            return

        self._process_column_select(select_expression, table_name)

    def _process_count(self, table_name: str) -> None:
        root_page_offset = self._get_root_page_offset(table_name)
        row_count = self._database_processor.get_number_of_tables(root_page_offset)

        print(row_count)

    def _process_column_select(
        self,
        select_expression: str,
        table_name: str,
    ) -> None:
        record_offset = self._get_offset_to_target_record(table_name)

        create_table_sql = (
            self._database_processor
            .get_sql_from_record_at_offset(record_offset)
        )

        column_names = self._get_column_names_in_order(create_table_sql)
        column_index = column_names.index(select_expression)

        root_page_offset = self._get_root_page_offset_from_record(record_offset)

        cell_count = self._database_processor.get_number_of_tables(
            root_page_offset
        )

        cell_contents = (
            self._database_processor
            .get_cell_content_array_from_rootpage_offset(
                root_page_offset,
                cell_count,
                column_names,
            )
        )

        for cell_content in cell_contents:
            print(cell_content[column_index].decode("utf-8"))

    def _parse_select(self, sql: str) -> tuple[str, str]:
        _, select_expression, _, table_name = sql.split()
        return select_expression, table_name

    def _get_root_page_offset(self, table_name: str) -> int:
        record_offset = self._get_offset_to_target_record(table_name)
        return self._get_root_page_offset_from_record(record_offset)

    def _get_root_page_offset_from_record(self, record_offset: int) -> int:
        root_page = (
            self._database_processor
            .get_root_page_from_record_at_offset(record_offset)
        )

        page_size = self._database_processor.get_page_size()

        return (root_page - 1) * page_size

    def _get_column_names_in_order(self, sql: str) -> List[str]:
        start_parenthesis = sql.index("(")
        end_parenthesis = sql.index(")")

        definitions = sql[start_parenthesis + 1:end_parenthesis].split(",")

        return [
            definition.strip().split()[0]
            for definition in definitions
        ]

    def _get_offset_to_target_record(self, table_name: str) -> int:
        cell_pointer_array_offsets = (
            self._database_processor
            .get_cell_pointer_array_offsets()
        )

        for offset in cell_pointer_array_offsets:
            table_name_at_offset = (
                self._database_processor
                .get_table_name_from_record_at_offset(offset)
            )

            if table_name == table_name_at_offset:
                return offset

        raise ValueError(f"Table not found: {table_name}")