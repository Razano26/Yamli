""" Module pour lancer le parsing YAML en CLI et l'application Streamlit. """

import argparse
import yaml  # Utilisé pour valider la syntaxe YAML
import streamlit.web.cli as stcli
from yamli.parser import YAMLParser


def validate_yaml_file(file_path):
    """Valide uniquement la syntaxe d'un fichier YAML."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            yaml.safe_load(file)  # Vérifie la syntaxe YAML
        print(f"✅ Syntaxe valide : {file_path}")
    except yaml.YAMLError as e:
        print(
            f"❌ Erreur de syntaxe YAML dans {file_path} :\n----------------\n{e}\n----------------"
        )
    except Exception as e:  # pylint: disable=broad-except
        print(f"❌ Erreur inattendue : {e}")


def parse_yaml_file(file_path):
    """Parse un fichier YAML et affiche les résultats en CLI."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    parser = YAMLParser()
    document = parser.parse_document(lines)
    parser.validate_document(document)


def serve():
    """Lance l'application Streamlit en tant que serveur."""
    stcli.main(["run", "yamli/app.py"])


def main():
    """Fonction principale pour le parsing en CLI et le serveur Streamlit."""
    parser = argparse.ArgumentParser(
        description="Parseur YAML CLI et serveur Streamlit"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Commande pour le parsing en CLI
    parse_parser = subparsers.add_parser("parse", help="Parse un fichier YAML en CLI")
    parse_parser.add_argument("file", help="Chemin du fichier YAML à parser")

    # Commande pour valider uniquement la syntaxe
    validate_parser = subparsers.add_parser(
        "validate", help="Valide uniquement la syntaxe d'un fichier YAML"
    )
    validate_parser.add_argument("file", help="Chemin du fichier YAML à valider")

    # Commande pour lancer Streamlit
    subparsers.add_parser("serve", help="Lancer l'application Streamlit")

    args = parser.parse_args()

    if args.command == "parse":
        parse_yaml_file(args.file)
    elif args.command == "validate":
        validate_yaml_file(args.file)
    elif args.command == "serve":
        serve()


if __name__ == "__main__":
    main()
