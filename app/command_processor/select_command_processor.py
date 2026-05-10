from app.database_processor.database_processor import DatabaseProcessor


class SelectCommandProcessor:
    def __init__(self, database_processor: DatabaseProcessor) -> None:
        self._database_processor = database_processor
    
    def process(self, sql: str):
        self._database_processor.