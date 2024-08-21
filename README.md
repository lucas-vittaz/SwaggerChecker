# Swagger Validator

## Description

**Swagger Validator** est un outil conçu pour valider des fichiers Swagger (OpenAPI) en fonction de règles spécifiques définies dans un fichier JSON. Les équipes de développement peuvent s'assurer que leurs spécifications d'API respectent des normes internes ou des standards. Grâce à son interface utilisateur, cet outil permet de valider rapidement et efficacement les chemins d'API, les paramètres de requête, les en-têtes, et les réponses ect.

## Fonctionnalités

- **Validation des chemins** : Vérifiez que les chemins d'API ne contiennent pas de mots réservés interdits.
- **Validation des paramètres de requête** : Assurez-vous que les paramètres de requête sont présents et correctement typés.
- **Validation des en-têtes** : Vérifiez que les en-têtes requis sont définis et correctement typés.
- **Validation des réponses** : Contrôlez que les réponses suivent le schéma attendu pour chaque code de statut HTTP.

## Avantages

- **Facilité d'utilisation** : Interface utilisateur intuitive permettant de valider les fichiers Swagger sans effort.
- **Personnalisation** : Les règles de validation sont définies dans un fichier JSON, ce qui vous permet de les adapter facilement à vos besoins spécifiques.
- **Intégration CI/CD** : Intégrez cet outil dans vos pipelines pour automatiser la validation des spécifications d'API.

## Prérequis

- **Python 3.8+**
- **Tkinter** (pour l'interface graphique)
- **Dépendances Python** : Voir `requirements.txt`

## Installation

1. Clonez ce dépôt sur votre machine locale :
    ```bash
    git clone https://github.com/votreutilisateur/swagger-validator.git
    cd swagger-validator
    ```

2. Créez un environnement virtuel et activez-le :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

### 1. Exécuter via Python

Pour démarrer l'application via Python :

```bash
python main.py
