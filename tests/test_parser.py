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


def test_validate_yaml_file_valid():
    """Test que la validation réussit avec un fichier YAML valide."""
    valid_yaml = """
    name: Example
    version: 1.0
    """
    with open("tests/valid.yaml", "w", encoding="utf-8") as file:
        file.write(valid_yaml)

    try:
        validate_yaml_file("tests/valid.yaml")
    except Exception:  # pylint: disable=broad-except
        pytest.fail("La validation ne devrait pas échouer avec un fichier valide.")


def test_validate_yaml_file_invalid(capsys):
    """Test que la validation échoue avec un fichier YAML invalide."""
    invalid_yaml = """
    name: Example
    version: 1.0
      extra_indent: wrong
    """
    invalid_file_path = "tests/invalid.yaml"
    with open(invalid_file_path, "w", encoding="utf-8") as file:
        file.write(invalid_yaml)

    validate_yaml_file(invalid_file_path)

    captured = capsys.readouterr()
    assert "❌ Erreur de syntaxe YAML dans" in captured.out
    assert invalid_file_path in captured.out


def test_validate_yaml_file_unexpected_error(capsys, mocker):
    """Mock un scénario où une erreur inattendue se produit"""
    mocker.patch("builtins.open", side_effect=Exception("Erreur inattendue"))
    fake_file_path = "/fake/path/to/file.yaml"

    # Appelle la fonction
    validate_yaml_file(fake_file_path)

    # Capture et vérifie la sortie
    captured = capsys.readouterr()
    assert "❌ Erreur inattendue" in captured.out
    assert "Erreur inattendue" in captured.out
