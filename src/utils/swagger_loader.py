import json
import yaml

def load_swagger(file_path):
    """
    Charge un fichier Swagger au format JSON ou YAML.

    Args:
        file_path (str): Chemin vers le fichier Swagger.

    Returns:
        dict: Contenu du fichier Swagger sous forme de dictionnaire.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            if file_path.endswith('.json'):
                return json.load(file)
            elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(file)
            else:
                raise ValueError("Unsupported file format. Please provide a .json or .yaml file.")
    except Exception as e:
        raise ValueError(f"Failed to load Swagger file: {str(e)}")
