import re


class YAMLParser:
    """
    Un parseur simplifié pour analyser des fichiers YAML et valider leur structure.
    """

    def __init__(self):
        self.stack = []  # Pile pour gérer les contextes imbriqués

    def parse_document(self, lines):
        """
        Parse un document YAML à partir d'une liste de lignes.

        Arguments:
        lines -- Liste des lignes du document YAML.

        Retourne:
        parsed_data -- Structure de données analysée.
        """
        parsed_data = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().endswith(": |"):  # Détection du début d'un bloc `|`
                key = line.split(":")[0].strip()
                self.stack.append(("literal_block_start", key))  # Empiler le contexte
                literal_block, end_index = self.parse_literal_block(lines, i + 1)
                self.stack.pop()  # Dépiler après traitement
                parsed_data.append(("literal_block", key, literal_block))
                i = end_index  # Avancer à la fin du bloc
            else:
                parsed_line = self.parse_line(line)
                if parsed_line is not None:
                    parsed_data.append(parsed_line)
            i += 1
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

        if line.strip().startswith("- "):  # Cas d'un élément de liste
            item = line.strip()[2:]  # Supprimer "- "
            return ("list_item", item)

        match = re.match(r"(\w+):\s*(.*)", line.strip())  # Correspondance clé-valeur
        if match:
            key, value = match.groups()
            if value == "|":
                return None  # La gestion du bloc littéral est séparée
            else:
                return ("key_value", key, value)

        raise SyntaxError(f"Erreur de syntaxe YAML à la ligne: {line}")

    def parse_literal_block(self, lines, start_index):
        """
        Parse un bloc de texte YAML après un `|` et conserve les sauts de ligne et l'indentation.

        Arguments:
        lines -- Liste des lignes du document YAML.
        start_index -- Index de la première ligne après `|`.

        Retourne:
        tuple -- Texte du bloc et index de fin.
        """
        block = []
        initial_indent = len(lines[start_index - 1]) - len(
            lines[start_index - 1].lstrip()
        )

        for i in range(start_index, len(lines)):
            line = lines[i]
            current_indent = len(line) - len(line.lstrip())

            if current_indent > initial_indent or not line.strip():
                block.append(line.strip())  # Ajouter chaque ligne du bloc
            else:
                return "\n".join(block), i - 1  # Fin du bloc multi-lignes

        return "\n".join(block), len(lines) - 1

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
            elif element[0] == "literal_block":
                key, block = element[1], element[2]
                print(f"Bloc texte ({key}):\n{block}\n")


if __name__ == "__main__":
    import argparse

    def parse_yaml_file(filepath):
        with open(filepath, "r") as file:
            lines = file.readlines()

        parser = YAMLParser()
        document = parser.parse_document(lines)
        parser.validate_document(document)

    parser = argparse.ArgumentParser(description="Parse a YAML file.")
    parser.add_argument("file", help="Path to the YAML file to parse.")
    args = parser.parse_args()

    parse_yaml_file(args.file)
