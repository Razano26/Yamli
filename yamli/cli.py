""" Module pour lancer le parsing YAML en CLI et l'application Streamlit. """

import argparse
import streamlit.web.cli as stcli
from yamli.parser import YAMLParser


def validate_yaml_file(file_path):
    """Valide uniquement la syntaxe d'un fichier YAML."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        parser = YAMLParser()
        parser.parse_document(lines)
        print(f"✅ Syntaxe YAML valide pour le fichier : {file_path}")
    except SyntaxError as e:
        print(f"❌ Erreur de syntaxe dans le fichier : {file_path}\n  {e}")
    except Exception as e:
        print(f"❌ Une erreur inattendue s'est produite : {e}")


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
