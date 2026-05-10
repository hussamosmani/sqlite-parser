from database_processor.database_processor import DatabaseProcessor


class DbInfoCommandProcessor:

    def __init__(self, database_processor: DatabaseProcessor):
        self._database_processor = database_processor
    
    def process(self):
        page_size = self._database_processor.get_page_size()
        number_of_cells = self._database_processor.get_number_of_tables()
        
        print(f"database page size: {page_size}")
        print(f"number of tables: {number_of_cells}")
    