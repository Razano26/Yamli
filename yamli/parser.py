import re


class YAMLParser:
    """
    Un parseur simplifié pour analyser des fichiers YAML et valider leur structure.
    """

    def __init__(self):
        self.indentation_level = 0

    def parse_document(self, lines):
        """
        Parse un document YAML à partir d'une liste de lignes.

        Arguments:
        lines -- Liste des lignes du document YAML.

        Retourne:
        parsed_data -- Structure de données analysée.
        """
        parsed_data = []
        for line in lines:
            parsed_line = self.parse_line(line)
            if parsed_line is not None:
                parsed_data.append(parsed_line)
        return parsed_data

    def parse_line(self, line):
        """
        Parse une seule ligne YAML pour identifier la clé, la valeur, ou les éléments de liste.

        Arguments:
        line -- Ligne YAML à analyser.

        Retourne:
        tuple -- Identifie le type de l'élément et sa valeur.
        """
        line = line.rstrip()
        if not line or line.startswith("#"):  # Ignorer les lignes vides et commentaires
            return None

        current_indent = len(line) - len(line.lstrip())

        if line.strip().startswith("- "):  # Cas d'un élément de liste
            item = line.strip()[2:]  # Supprimer "- "
            return ("list_item", item)

        match = re.match(r"(\w+):\s*(.*)", line.strip())  # Correspondance clé-valeur
        if match:
            key, value = match.groups()
            if not value:
                value = None  # Accepter des valeurs vides
            return ("key_value", key, value)

        raise SyntaxError(f"Erreur de syntaxe YAML à la ligne: {line}")

    def validate_document(self, document):
        """
        Valide la structure du document analysé.

        Arguments:
        document -- Document analysé sous forme de liste d'éléments.
        """
        for element in document:
            if element[0] == "key_value":
                key, value = element[1], element[2]
                print(f"Clé: {key}, Valeur: {value}")
            elif element[0] == "list_item":
                print(f"Élément de liste: {element[1]}")


if __name__ == "__main__":
    with open("example.yaml", "r") as file:
        lines = file.readlines()

    parser = YAMLParser()
    document = parser.parse_document(lines)
    parser.validate_document(document)
