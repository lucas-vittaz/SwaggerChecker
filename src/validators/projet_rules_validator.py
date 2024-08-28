import os
import sys
import json

class ProjetRulesValidator:
    """
    Cette classe est utilisée pour valider un fichier Swagger (ou OpenAPI) par rapport à un ensemble de règles
    spécifiques définies dans un fichier de configuration JSON. Les règles incluent la vérification des chemins réservés,
    des paramètres de requête, des en-têtes et des réponses pour différentes méthodes HTTP.
    """

    def __init__(self, swagger_dict, swagger_text, rules_config_path=None):
        """
        Initialise la classe avec le dictionnaire Swagger et le texte Swagger. Charge également les règles de validation
        à partir d'un fichier JSON. Le chemin du fichier de règles est déterminé en fonction de l'environnement
        (exécutable ou script).

        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        :param rules_config_path: (optionnel) Chemin vers le fichier JSON contenant les règles de validation.
        """
        if rules_config_path is None:
            if getattr(sys, 'frozen', False):  # Si le programme est exécuté en tant qu'exécutable
                # Lorsque gelé, utiliser le répertoire temporaire et revenir au dossier de configuration
                base_path = sys._MEIPASS
                rules_config_path = os.path.join(base_path, 'config', 'projet_validation_rules.json')
            else:
                # Supposer que le dossier de configuration est à la racine du projet lors de l'exécution en tant que script
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                rules_config_path = os.path.join(base_path, 'config', 'projet_validation_rules.json')
           
        print(f"Loading validation rules from: {rules_config_path}")
        
        self.swagger_dict = swagger_dict
        self.swagger_text = swagger_text.splitlines()
        self.rules = self.load_validation_rules(rules_config_path)
        self.reserved_paths = self.rules.get("reserved_paths", [])

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

    def validate_reserved_paths(self):
        """
        Vérifie que les chemins définis dans le Swagger ne contiennent pas de mots réservés définis dans les règles de validation.

        :return: Une liste d'erreurs trouvées lors de la validation des chemins réservés.
        """
        errors = []
        for path in self.swagger_dict.get('paths', {}).keys():
            for reserved in self.reserved_paths:
                if reserved in path.split('/'):
                    line_number = self._find_line_number(path)
                    errors.append(f"Le chemin '{path}' contient un mot réservé '{reserved}' (ligne {line_number})")
        return errors

    def validate_query_parameters(self, method):
        """
        Valide les paramètres de requête pour une méthode HTTP donnée en fonction des règles définies.

        :param method: Méthode HTTP (GET, POST, etc.) pour laquelle les paramètres de requête doivent être validés.
        :return: Une liste d'erreurs trouvées lors de la validation des paramètres de requête.
        """
        errors = []
        method_rules = self.rules.get(method, {})
        
        if isinstance(method_rules, dict):  # Assurez-vous que method_rules est un dictionnaire
            query_parameters = method_rules.get("query_parameters", [])
            for rule in query_parameters:
                param_name = rule["name"]
                parameter = self._find_parameter(param_name, 'query', method)
                if parameter:
                    if rule.get("required", False) and not parameter.get('required', False):
                        line_number = self._find_line_number(param_name)
                        errors.append(f"Paramètre de requête '{param_name}' obligatoire manquant dans {method} (ligne {line_number})")
                    if "type" in rule and parameter.get('schema', {}).get('type') != rule["type"]:
                        line_number = self._find_line_number(param_name)
                        errors.append(f"Type incorrect pour le paramètre de requête '{param_name}' dans {method} (ligne {line_number}), attendu: {rule['type']}")
                else:
                    line_number = self._find_line_number(param_name)
                    errors.append(f"Paramètre de requête '{param_name}' manquant dans {method} (ligne {line_number})")
        else:
            print(f"Attention: Les règles pour {method} ne sont pas un dictionnaire.")
        
        return errors

    def validate_headers(self, method):
        """
        Valide les en-têtes pour une méthode HTTP donnée en fonction des règles définies.

        :param method: Méthode HTTP (GET, POST, etc.) pour laquelle les en-têtes doivent être validés.
        :return: Une liste d'erreurs trouvées lors de la validation des en-têtes.
        """
        errors = []
        method_rules = self.rules.get(method, {})

        if isinstance(method_rules, dict):  # Assurez-vous que method_rules est un dictionnaire
            headers = method_rules.get("headers", [])
            for rule in headers:
                header_name = rule["name"]
                header = self._find_parameter(header_name, 'header', method)
                if header:
                    if rule.get("required", False):
                        line_number = self._find_line_number(header_name)
                        errors.append(f"Header '{header_name}' non obligatoire mais devrait l'être dans {method} (ligne {line_number})")
                    if "type" in rule and header.get('schema', {}).get('type') != rule["type"]:
                        line_number = self._find_line_number(header_name)
                        errors.append(f"Type incorrect pour le header '{header_name}' dans {method} (ligne {line_number}), attendu: {rule['type']}")
                else:
                    line_number = self._find_line_number(header_name)
                    errors.append(f"Header '{header_name}' manquant dans {method} (ligne {line_number})")
        else:
            print(f"Attention: Les règles pour {method} ne sont pas un dictionnaire.")
        
        return errors

    def validate_responses(self, method):
        """
        Valide les réponses pour une méthode HTTP donnée en fonction des règles définies.

        :param method: Méthode HTTP (GET, POST, etc.) pour laquelle les réponses doivent être validées.
        :return: Une liste d'erreurs trouvées lors de la validation des réponses.
        """
        errors = []
        method_rules = self.rules.get(method, {})
        for rule in method_rules.get("responses", []):
            response_code = rule["response_code"]
            response_schema = self._find_response_schema(response_code, method)
            if response_schema:
                if not self._validate_json_schema(response_schema, rule.get("format", {})):
                    line_number = self._find_line_number(f'"{response_code}":')
                    errors.append(f"Format de réponse incorrect pour {response_code} dans {method} (ligne {line_number})")
            else:
                line_number = self._find_line_number(f'"{response_code}":')
                errors.append(f"Gestion de l'erreur {response_code} manquante dans {method} (ligne {line_number})")
        return errors

    def _find_parameter(self, name, location, method):
        """
        Recherche un paramètre spécifique par nom et emplacement (par exemple, dans la requête ou dans l'en-tête)
        pour une méthode HTTP donnée dans le Swagger.

        :param name: Nom du paramètre à rechercher.
        :param location: Emplacement du paramètre (query, header, etc.).
        :param method: Méthode HTTP pour laquelle le paramètre doit être recherché.
        :return: Le paramètre trouvé ou None s'il n'est pas trouvé.
        """
        for path_data in self.swagger_dict.get('paths', {}).values():
            for method_name, method_data in path_data.items():
                if method_name.lower() == method.lower():
                    for param in method_data.get('parameters', []):
                        if param.get('name') == name and param.get('in') == location:
                            return param
        return None

    def _find_response_schema(self, response_code, method):
        """
        Recherche le schéma de réponse pour un code de réponse spécifique dans une méthode HTTP donnée.

        :param response_code: Code de réponse HTTP à rechercher (200, 404, etc.).
        :param method: Méthode HTTP pour laquelle le schéma de réponse doit être recherché.
        :return: Le schéma de la réponse ou None s'il n'est pas trouvé.
        """
        for path_data in self.swagger_dict.get('paths', {}).values():
            for method_name, method_data in path_data.items():
                if method_name.lower() == method.lower():
                    response = method_data.get('responses', {}).get(str(response_code), {})
                    if response:
                        return response.get('content', {}).get('application/json', {}).get('schema', {})
        return None

    def _validate_json_schema(self, actual, expected):
        """
        Compare un schéma JSON réel avec un schéma attendu pour vérifier s'ils correspondent.

        :param actual: Schéma JSON actuel tel que défini dans le Swagger.
        :param expected: Schéma JSON attendu tel que défini dans les règles de validation.
        :return: True si le schéma réel correspond au schéma attendu, False sinon.
        """
        if actual.get('type') != expected.get('type'):
            return False
        for prop, prop_spec in expected.get('properties', {}).items():
            if prop not in actual.get('properties', {}):
                return False
            if actual['properties'][prop].get('type') != prop_spec.get('type'):
                return False
        for req in expected.get('required', []):
            if req not in actual.get('required', []):
                return False
        return True

    def validate(self):
        """
        Exécute toutes les validations pour les chemins réservés, les paramètres de requête, les en-têtes et les réponses.

        :return: Un tuple (bool, str) où le booléen indique si le Swagger est conforme, et la chaîne contient les détails des erreurs ou un message de succès.
        """
        errors = []
        errors.extend(self.validate_reserved_paths())
        
        for method, method_rules in self.rules.items():
            if isinstance(method_rules, dict):  # Vérifier que method_rules est un dictionnaire
                errors.extend(self.validate_query_parameters(method))
                errors.extend(self.validate_headers(method))
                errors.extend(self.validate_responses(method))
            else:
                print(f"Attention: Les règles pour {method} ne sont pas un dictionnaire.")
        
        if errors:
            return False, "\n".join(errors)
        return True, "Swagger conforme aux normes du projet."

    def _find_line_number(self, keyword):
        """
        Recherche un mot-clé spécifique dans le texte brut du Swagger et retourne le numéro de la ligne où il apparaît.

        :param keyword: Mot-clé à rechercher dans le texte du Swagger.
        :return: Le numéro de la ligne où le mot-clé a été trouvé, ou "inconnue" s'il n'a pas été trouvé.
        """
        for index, line in enumerate(self.swagger_text, start=1):
            if keyword in line:
                return index
        return "inconnue"
