from .argument_parser_interface import ArgumentParserInterface, Command
class ArgumentParser(ArgumentParserInterface):

    def parse_command(self, command: str) -> Command:
        if command == ".dbinfo":
            return Command.DB_INFO
        elif command == ".tables":
            return Command.TABLES
        elif command == "SELECT":
            return Command.SELECT
        return Command.NOT_SUPPORTED