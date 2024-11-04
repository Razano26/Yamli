import streamlit as st
from yamli.parser import YAMLParser
import yaml  # Bibliothèque pour afficher la structure YAML en format JSON-like
from anytree import Node, RenderTree  # Pour visualiser la structure en arbre
import io

# Configuration de la page
st.set_page_config(page_title="YAML Live Parser", page_icon="📝", layout="wide")

st.title("📝 Live YAML Parser")
st.markdown("Interprétez du YAML en direct et visualisez la structure des données.")

# Texte YAML de démonstration par défaut
default_yaml = """
name: ExampleProject
version: 1.0
description: |
  Ceci est une description multi-lignes
  du projet. Elle conserve les sauts de ligne
  et la structure du texte.
authors:
  - Alice
  - Bob
  - Carol

database:
  type: postgres
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: secretpassword

notes: |
  Ceci est une autre note multi-lignes.
  Elle peut contenir plusieurs paragraphes et
  des retours à la ligne.
"""

# Barre latérale pour les actions et informations
st.sidebar.title("Options")
st.sidebar.markdown("Utilisez les options ci-dessous pour personnaliser l'entrée YAML.")
reset_button = st.sidebar.button("🔄 Réinitialiser le texte")
show_example = st.sidebar.checkbox("Afficher un exemple de YAML", value=True)

# Zone de texte principale avec option de réinitialisation
yaml_input = st.text_area(
    "Entrez votre YAML ici 👇", default_yaml if show_example else "", height=300
)

if reset_button:
    yaml_input = default_yaml  # Réinitialise le texte à l'exemple par défaut

# Séparateur pour la sortie
st.markdown("---")

if yaml_input:
    # Divise le texte en lignes pour l'analyse
    lines = yaml_input.splitlines()

    # Initialise le parseur et interprète les lignes de YAML
    parser = YAMLParser()
    try:
        document = parser.parse_document(lines)

        # Affiche les résultats du parsing
        st.subheader("📄 Résultats du Parsing")
        st.success("Parsing réussi !")

        # Fonction de création d'arbre
        def build_tree(node, data):
            """Construit un arbre à partir de données YAML imbriquées."""
            if isinstance(data, dict):
                for key, value in data.items():
                    child = Node(f"{key}: {type(value).__name__}", parent=node)
                    build_tree(child, value)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    child = Node(f"Item {i}: {type(item).__name__}", parent=node)
                    build_tree(child, item)
            else:
                Node(f"{data} ({type(data).__name__})", parent=node)

        # Créer un arbre racine et remplir la structure YAML
        root = Node("Root")
        yaml_data = yaml.safe_load(yaml_input)  # Charger YAML comme structure Python
        build_tree(root, yaml_data)

        # Affiche la structure de l'arbre
        st.subheader("🌳 Structure YAML en Arbre")
        tree_text = "\n".join(
            [f"{pre}{node.name}" for pre, _, node in RenderTree(root)]
        )
        st.text(tree_text)

        # Affichage formaté de la structure des données YAML
        st.subheader("🧾 Détails des Clés et Types")
        for element in document:
            if element[0] == "key_value":
                st.write(
                    f"🔑 **Clé**: `{element[1]}`, **Valeur**: `{element[2]}` (Type: {type(element[2]).__name__})"
                )
            elif element[0] == "list_item":
                st.write(
                    f"📋 **Élément de liste**: `{element[1]}` (Type: {type(element[1]).__name__})"
                )

        # Bouton pour télécharger le YAML en fichier
        yaml_buffer = io.StringIO()
        yaml.dump(yaml_data, yaml_buffer)
        st.download_button(
            "💾 Télécharger le YAML formaté",
            yaml_buffer.getvalue(),
            file_name="parsed_yaml.yaml",
        )

    except yaml.YAMLError as e:
        st.error(f"❌ Erreur de syntaxe YAML : {e}")
    except Exception as e:
        st.error(f"❌ Erreur lors du parsing : {e}")
else:
    st.info("Veuillez entrer du YAML pour voir les résultats.")
