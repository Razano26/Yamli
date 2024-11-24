import argparse
import streamlit.web.cli as stcli
from yamli.parser import YAMLParser


def parse_yaml_file(file_path):
    """Parse un fichier YAML et affiche les résultats en CLI."""
    with open(file_path, "r") as file:
        lines = file.readlines()
    parser = YAMLParser()
    document = parser.parse_document(lines)
    parser.validate_document(document)


def serve():
    """Lance l'application Streamlit en tant que serveur."""
    stcli.main(["run", "yamli/app.py"])


def main():
    parser = argparse.ArgumentParser(
        description="Parseur YAML CLI et serveur Streamlit"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Commande pour le parsing en CLI
    parse_parser = subparsers.add_parser("parse", help="Parse un fichier YAML en CLI")
    parse_parser.add_argument("file", help="Chemin du fichier YAML à parser")

    # Commande pour lancer Streamlit
    subparsers.add_parser("serve", help="Lancer l'application Streamlit")

    args = parser.parse_args()

    if args.command == "parse":
        parse_yaml_file(args.file)
    elif args.command == "serve":
        serve()


if __name__ == "__main__":
    main()
