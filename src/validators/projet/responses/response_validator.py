from ..base_validator import BaseValidator

class ResponseValidator(BaseValidator):
    """
    Valide les schémas de réponse définis dans le Swagger.
    """

    def validate_responses(self, method, method_rules):
        """
        Valide les réponses pour une méthode HTTP donnée en fonction des règles définies.
        
        :param method: Méthode HTTP pour laquelle les réponses doivent être validées.
        :param method_rules: Règles spécifiques à la méthode.
        :return: Une liste d'erreurs trouvées lors de la validation des réponses.
        """
        errors = []
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
