import os
import sys
import json

from .path_validator import PathValidator
from .header_validator import HeaderValidator
from .query_param_validator import QueryParamValidator
from .info_validator import InfoValidator
from .response_validator import ResponseValidator
from .special_character_validator import SpecialCharacterValidator

class ProjetRulesValidator:
    """
    Classe principale pour valider un fichier Swagger (ou OpenAPI) par rapport à un ensemble de règles spécifiques.
    """

    def __init__(self, swagger_dict, swagger_text, rules_config_path=None):
        """
        Initialise la classe avec les différents validateurs.
        
        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        :param rules_config_path: (optionnel) Chemin vers le fichier JSON contenant les règles de validation.
        """
        if rules_config_path is None:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
                rules_config_path = os.path.join(base_path, 'config', 'projet_validation_rules.json')
            else:
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..'))
                rules_config_path = os.path.join(base_path, 'config', 'projet_validation_rules.json')

        print(f"Loading validation rules from: {rules_config_path}")
        
        self.swagger_dict = swagger_dict
        self.swagger_text = swagger_text.splitlines()
        self.rules = self.load_validation_rules(rules_config_path)

        special_characters = self.rules.get("special_characters", [])

        self.path_validator = PathValidator(swagger_dict, swagger_text, self.rules.get("reserved_paths", []))
        self.header_validator = HeaderValidator(swagger_dict, swagger_text, self.rules.get("reserved_headers", []))
        self.query_param_validator = QueryParamValidator(swagger_dict, swagger_text, self.rules.get("reserved_query_parameters", []))
        self.info_validator = InfoValidator(swagger_dict, swagger_text)
        self.response_validator = ResponseValidator(swagger_dict, swagger_text)
        self.special_character_validator = SpecialCharacterValidator(swagger_dict, swagger_text, special_characters)

    def load_validation_rules(self, filepath):
        """
        Charge les règles de validation à partir du fichier JSON spécifié.
        
        :param filepath: Chemin complet vers le fichier JSON contenant les règles de validation.
        :raises FileNotFoundError: Si le fichier n'est pas trouvé.
        :return: Un dictionnaire représentant les règles de validation chargées.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Validation rules file not found: {filepath}")
        with open(filepath, 'r') as file:
            return json.load(file)


    def validate(self):
        """
        Exécute toutes les validations définies dans les validateurs.
        
        :return: Un tuple (bool, str) où le booléen indique si le Swagger est conforme, et la chaîne contient les détails des erreurs ou un message de succès.
        """
        errors = []
        errors.extend(self.path_validator.validate_reserved_paths())
        errors.extend(self.header_validator.validate_reserved_headers())
        errors.extend(self.query_param_validator.validate_reserved_query_parameters())
        errors.extend(self.info_validator.validate_title())
        errors.extend(self.info_validator.validate_version())
        errors.extend(self.info_validator.validate_description())
        errors.extend(self.info_validator.validate_basepath())
        errors.extend(self.special_character_validator.validate_all_values())

        for method, method_rules in self.rules.items():
            if isinstance(method_rules, dict):
                errors.extend(self.query_param_validator.validate_reserved_query_parameters())
                errors.extend(self.header_validator.validate_reserved_headers())
                errors.extend(self.response_validator.validate_responses(method, method_rules))
            else:
                print(f"Attention: Les règles pour {method} ne sont pas un dictionnaire.")

        if errors:
            return False, "\n".join(errors)
        return True, "Swagger conforme aux normes du projet."
