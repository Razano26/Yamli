""" Tests unitaires pour le module yamli.parser """

import yaml
from anytree import Node

from yamli.app import build_tree
from yamli.parser import YAMLParser


def test_parse_key_value():
    """ Teste la méthode de parsing pour une paire clé-valeur. """
    parser = YAMLParser()
    result = parser.parse_line("name: ExampleProject")
    assert result == ("key_value", "name", "ExampleProject")


def test_parse_list_item():
    """ Teste la méthode de parsing pour un élément de liste. """
    parser = YAMLParser()
    result = parser.parse_line("- item1")
    assert result == ("list_item", "item1")


def test_invalid_yaml_syntax():
    """ Teste une erreur de syntaxe YAML. """
    parser = YAMLParser()
    invalid_yaml = ["name: ExampleProject", "- item1", "invalid line"]
    try:
        parser.parse_document(invalid_yaml)
        assert False, "Expected a parsing error"
    except SyntaxError:
        pass  # Erreur attendue


def test_tree_structure():
    """Test que la structure de l'arbre est correcte pour des données imbriquées."""
    yaml_data = """
    database:
      type: postgres
      credentials:
        username: admin
        password: secret
    """
    data = yaml.safe_load(yaml_data)
    root = Node("Root")
    build_tree(root, data)
    assert len(root.children) == 1  # 'database' est la racine
    assert root.children[0].name == "database: dict"
    assert root.children[0].children[0].name == "type: str"
    assert root.children[0].children[1].name == "credentials: dict"
