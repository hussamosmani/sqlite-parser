from typing import List, Optional, Tuple

from app.database_processor.database_processor import DatabaseProcessor


class SelectCommandProcessor:
    COUNT_ALL_KEYWORDS_UPPER = "COUNT(*)"
    COUNT_ALL_KEYWORDS_LOWER = "count(*)"

    def __init__(self, database_processor: DatabaseProcessor) -> None:
        self._database_processor = database_processor

    def process(self, sql: str) -> None:
        select_expression, table_name, parsed_wear_clause = self._parse_select(sql)

        if select_expression[0] in [self.COUNT_ALL_KEYWORDS_UPPER,self.COUNT_ALL_KEYWORDS_LOWER]:
            self._process_count(table_name)
            return

        self._process_column_select(select_expression, table_name, parsed_wear_clause)

    def _process_count(self, table_name: str) -> None:
        root_page_offset = self._get_root_page_offset(table_name)
        row_count = self._database_processor.get_number_of_tables(root_page_offset)


    def _process_column_select(
        self,
        select_expression: List[str],
        table_name: str,
        parsed_wear_clause: Optional[tuple[str,str]]
    ) -> None:
        record_offset = self._get_offset_to_target_record(table_name)

        create_table_sql = (
            self._database_processor
            .get_sql_from_record_at_offset(record_offset)
        )

        column_names = self._get_column_names_in_order(create_table_sql)

        parsed_where_column_index,parsed_column_where_value = None, None
        if parsed_wear_clause:
            parsed_column_where_column,parsed_column_where_value = parsed_wear_clause
            parsed_where_column_index = column_names.index(parsed_column_where_column) - 1

        expression_to_print_dict = {}
        for column_name in select_expression:
            column_index = column_names.index(column_name)

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
            i = 0

            for cell_content in cell_contents:
                if i not in expression_to_print_dict:
                    expression_to_print_dict[i] = []
                expression_to_print_dict[i].append(cell_content[column_index].decode("utf-8"))
                i+=1
        for expression in expression_to_print_dict:
            if parsed_where_column_index and parsed_column_where_value != expression_to_print_dict[expression][parsed_where_column_index]:
                continue

            print("|".join(expression_to_print_dict[expression]))

    def _parse_select(self, sql: str) -> tuple[List[str], str, Optional[tuple[str,str]]]:
        get_columns_to_parse = self._get_columns_to_parse(sql)
        table_name = self._get_table_name(sql)
        parsed_where_clause = self._parse_wear_clause(sql)
        return get_columns_to_parse, table_name,parsed_where_clause 

    def _get_columns_to_parse(self,sql:str):
        normalized_sql = sql.upper()
        from_keyword = "FROM"
        select_keyword = "SELECT"
        index_of_from = normalized_sql.index(from_keyword) 
        select_expression = sql[len(select_keyword):index_of_from]
        columns_to_select = select_expression.split(",")
        for i in range(0,len(columns_to_select)):
            columns_to_select[i] = columns_to_select[i].strip()
        return columns_to_select

    def _get_table_name(self, sql:str) -> str:
        where_keyword = "WHERE"
        normalized_sql = sql.upper() 
        where_index = normalized_sql.find(where_keyword) 
        if where_index == -1:
            return sql.split()[-1]

        from_keyword = "FROM"
        index_of_from = normalized_sql.index(from_keyword) 
        table_name = sql[len(from_keyword) + index_of_from: where_index ]
        return table_name.strip()

    def _parse_wear_clause(self, sql: str) -> Optional[Tuple[str,str]]:
        where_keyword = "WHERE"
        normalized_sql = sql.upper()
        index_of_where = normalized_sql.find(where_keyword)
        if index_of_where == -1:
            return
        where_expression = sql[index_of_where + len(where_keyword):]
        target_column, target_value = where_expression.split("=")
        return target_column.strip(), target_value.strip()[1:-1]


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