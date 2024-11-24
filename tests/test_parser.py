""" Tests unitaires pour le module yamli.parser """

import pytest
import yaml
from anytree import Node

from yamli.app import build_tree
from yamli.cli import validate_yaml_file
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


def test_validate_yaml_file_valid(capsys):
    """Test que la validation réussit avec un fichier YAML valide."""
    valid_file_path = "tests/valid.yaml"

    validate_yaml_file(valid_file_path)
    # On s'attend à ce que la validation réussisse sans erreur
    # et que le message de succès soit affiché
    captured = capsys.readouterr()
    assert "✅ Syntaxe YAML valide pour le fichier" in captured.out
    assert valid_file_path in captured.out


def test_validate_yaml_file_invalid(capsys):
    """Test que la validation échoue avec un fichier YAML invalide."""
    invalid_file_path = "tests/invalid.yaml"

    validate_yaml_file(invalid_file_path)

    captured = capsys.readouterr()
    assert "❌ Erreur de syntaxe dans" in captured.out
    assert invalid_file_path in captured.out


def test_invalid_syntax_unclosed_list():
    """Test une erreur de liste non fermée dans un fichier YAML."""
    invalid_yaml = "invalid: [unclosed_list\n"
    parser = YAMLParser()
    with pytest.raises(SyntaxError, match="Erreur de syntaxe YAML"):
        parser.parse_document(invalid_yaml.splitlines())
