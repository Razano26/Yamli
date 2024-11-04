import re


class YAMLParser:
    def __init__(self):
        self.indentation_level = 0

    def parse_document(self, lines):
        """Parse a YAML document from a list of lines."""
        parsed_data = []
        for line in lines:
            parsed_line = self.parse_line(line)
            if parsed_line is not None:
                parsed_data.append(parsed_line)
        return parsed_data

    def parse_line(self, line):
        """Parse a single line of YAML."""
        line = line.rstrip()
        if not line or line.startswith("#"):  # Skip empty lines and comments
            return None

        current_indent = len(line) - len(line.lstrip())

        if line.strip().startswith("- "):  # List item
            item = line.strip()[2:]  # Remove "- "
            return ("list_item", item)

        match = re.match(r"(\w+):\s*(.*)", line.strip())  # Key-value match
        if match:
            key, value = match.groups()
            if not value:
                value = None  # Allow empty values
            return ("key_value", key, value)

        raise SyntaxError(f"Invalid YAML syntax at line: {line}")

    def validate_document(self, document):
        """Validate document structure."""
        for element in document:
            if element[0] == "key_value":
                key, value = element[1], element[2]
                print(f"Key: {key}, Value: {value}")
            elif element[0] == "list_item":
                print(f"List Item: {element[1]}")


if __name__ == "__main__":
    with open("example.yaml", "r") as file:
        lines = file.readlines()

    parser = YAMLParser()
    document = parser.parse_document(lines)
    parser.validate_document(document)
