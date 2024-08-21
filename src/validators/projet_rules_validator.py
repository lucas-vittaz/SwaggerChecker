import os
import sys
import json

class ProjetRulesValidator:
    def __init__(self, swagger_dict, swagger_text, rules_config_path=None):
        if rules_config_path is None:
            if getattr(sys, 'frozen', False):  # If the program is running as an executable
                # When frozen, use the temporary directory and backtrack to the config folder
                base_path = sys._MEIPASS
                rules_config_path = os.path.join(base_path, 'config', 'projet_validation_rules.json')
            else:
                # Assume the config folder is in the project root when running as a script
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                rules_config_path = os.path.join(base_path, 'config', 'projet_validation_rules.json')
           
        print(f"Loading validation rules from: {rules_config_path}")
        
        self.swagger_dict = swagger_dict
        self.swagger_text = swagger_text.splitlines()
        self.rules = self.load_validation_rules(rules_config_path)
        self.reserved_paths = self.rules.get("reserved_paths", [])

    def load_validation_rules(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Validation rules file not found: {filepath}")
        with open(filepath, 'r') as file:
            return json.load(file)

    def validate_reserved_paths(self):
        errors = []
        for path in self.swagger_dict.get('paths', {}).keys():
            for reserved in self.reserved_paths:
                if reserved in path.split('/'):
                    line_number = self._find_line_number(path)
                    errors.append(f"Le chemin '{path}' contient un mot réservé '{reserved}' (ligne {line_number})")
        return errors

    def validate_query_parameters(self, method):
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
        errors = []
        method_rules = self.rules.get(method, {})

        if isinstance(method_rules, dict):  # Assurez-vous que method_rules est un dictionnaire
            headers = method_rules.get("headers", [])
            for rule in headers:
                header_name = rule["name"]
                header = self._find_parameter(header_name, 'header', method)
                if header:
                    if rule.get("required", False) and not header.get('required', False):
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
        for path_data in self.swagger_dict.get('paths', {}).values():
            for method_name, method_data in path_data.items():
                if method_name.lower() == method.lower():
                    for param in method_data.get('parameters', []):
                        if param.get('name') == name and param.get('in') == location:
                            return param
        return None

    def _find_response_schema(self, response_code, method):
        for path_data in self.swagger_dict.get('paths', {}).values():
            for method_name, method_data in path_data.items():
                if method_name.lower() == method.lower():
                    response = method_data.get('responses', {}).get(str(response_code), {})
                    if response:
                        return response.get('content', {}).get('application/json', {}).get('schema', {})
        return None

    def _validate_json_schema(self, actual, expected):
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
        for index, line in enumerate(self.swagger_text, start=1):
            if keyword in line:
                return index
        return "inconnue"
