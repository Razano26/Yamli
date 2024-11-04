# Yamli

## Description
**Yamli** est un parseur simple pour le langage YAML, construit en Python et géré avec Poetry. Ce projet inclut une interface en ligne de commande (CLI) pour analyser les fichiers YAML et une interface web interactive via Streamlit, permettant de visualiser la structure YAML en temps réel et d'explorer les imbrications sous forme d'arbre.

## Grammaire YAML Simplifiée

Voici la grammaire simplifiée utilisée par le parseur **Yamli** pour interpréter les fichiers YAML.

### Structure Générale
- Un fichier YAML est composé d'éléments qui peuvent être des paires clé-valeur, des listes ou des dictionnaires imbriqués.
- La structure est définie par l'indentation (espaces).

### Grammaire en BNF

```bnf
<document> ::= <element> | <element> <document>
<element> ::= <key_value> | <list>
<key_value> ::= <key> ":" <value>
<list> ::= "-" <value>
<key> ::= <string>
<value> ::= <string> | <number> | "true" | "false" | "null" | <list> | <key_value>
```

### Explication de la Grammaire

1. **Document** : Un document YAML est une collection d'éléments.
2. **Élément** : Un élément peut être une paire clé-valeur ou un élément de liste.
3. **Paires clé-valeur** : Composées d'une clé suivie de `:` et d'une valeur.
4. **Listes** : Un élément de liste commence par `-` suivi de la valeur.
5. **Clés et Valeurs** : Les clés sont des chaînes, et les valeurs peuvent être de plusieurs types : chaîne, nombre, booléen (`true`, `false`), null, ou des listes/dictionnaires imbriqués.

### Exemples de Syntaxe Acceptée

```yaml
name: ExampleProject       # Clé-valeur
version: 1.0               # Clé-valeur avec un nombre
authors:                   # Clé avec une liste imbriquée
  - Alice
  - Bob
  - Carol
database:                  # Clé avec un dictionnaire imbriqué
  type: postgres
  credentials:
    username: admin
    password: secret
```

Cette grammaire permet au parseur de **Yamli** de reconnaître la plupart des structures YAML basiques tout en simplifiant l’analyse.

## Organisation des Fichiers
```plaintext
├── .gitignore               # Fichiers et dossiers ignorés par Git
├── LICENSE                  # Licence MIT
├── README.md                # Documentation du projet
├── example.yaml             # Exemple de fichier YAML pour les tests
├── poetry.lock              # Verrouillage des dépendances
├── pyproject.toml           # Configuration Poetry
├── tests                    # Dossier pour les tests unitaires
│   ├── __init__.py
│   └── test_parser.py       # Tests pour le parseur YAML et la structure en arbre
└── yamli                    # Dossier principal du code source
    ├── __init__.py
    ├── app.py               # Interface Streamlit pour visualisation en temps réel
    ├── cli.py               # Interface CLI pour exécuter le parseur et lancer Streamlit
    └── parser.py            # Parseur YAML principal
```

## Installation
1. Clonez ce dépôt :
    ```bash
    git clone <URL-du-dépôt>
    cd yamli
    ```

2. Installez les dépendances avec Poetry :
    ```bash
    poetry install
    ```

## Utilisation

### 1. Utilisation en CLI

Pour analyser un fichier YAML en ligne de commande, utilisez la commande suivante :

```bash
poetry run yamli parse example.yaml
```

### 2. Lancer l'Interface Web avec Streamlit

L'interface Streamlit permet une visualisation en temps réel. Pour lancer l'application :

```bash
poetry run yamli serve
```

Une fois lancée, ouvrez votre navigateur à l'adresse indiquée, généralement http://localhost:8501.

### Fonctionnalités de l'Interface Streamlit
- **Entrée YAML en temps réel** : Analysez le contenu YAML que vous saisissez dans une zone de texte.
- **Affichage en structure d’arbre** : Visualisation de la hiérarchie des données YAML sous forme d’arbre pour faciliter la compréhension des imbrications.
- **Validation des types** : Affichage des clés et types de données détectés (par exemple, chaîne, liste, dictionnaire).
- **Téléchargement du YAML formaté** : Téléchargez le contenu YAML modifié ou formaté via un bouton de téléchargement.
- **Exemple par défaut** : Un exemple YAML est chargé par défaut pour guider les utilisateurs.

## Tests

Les tests unitaires incluent :
- **Tests de syntaxe YAML** : Vérification des structures de base, comme les paires clé-valeur et les éléments de liste.
- **Tests de structure en arbre** : Validation de l'affichage hiérarchique des données YAML.
- **Tests d'erreurs** : Identification des erreurs de syntaxe et retour des messages d’erreur appropriés.

Pour exécuter les tests :

```bash
poetry run pytest
```

## Contribuer
Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, n’hésitez pas à ouvrir une pull request ou à signaler des problèmes.

## Licence
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
