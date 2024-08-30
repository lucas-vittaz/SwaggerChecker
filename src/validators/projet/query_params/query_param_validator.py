from ..base_validator import BaseValidator

class QueryParamValidator(BaseValidator):
    """
    Valide les paramètres de requête définis dans le Swagger en fonction des règles spécifiques pour chaque méthode HTTP.
    """

    def __init__(self, swagger_dict, swagger_text, rules):
        """
        Initialise le validateur avec les règles de validation des paramètres de requête pour chaque méthode HTTP.
        
        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        :param rules: Règles spécifiques pour chaque méthode HTTP.
        """
        super().__init__(swagger_dict, swagger_text)
        self.rules = rules

    def validate_query_parameters(self):
        """
        Valide les paramètres de requête dans le Swagger en fonction des règles spécifiées pour chaque méthode HTTP.
        
        :return: Une liste d'erreurs trouvées lors de la validation des paramètres de requête.
        """
        errors = []
        paths = self.swagger_dict.get('paths', {})

        for path, path_data in paths.items():
            for method, method_data in path_data.items():
                method_upper = method.upper()
                if method_upper in self.rules:
                    for rule in self.rules[method_upper].get("query_parameters", []):
                        param_name = rule["name"]
                        parameter = self._find_query_parameter(param_name, method_data.get('parameters', []))
                        if parameter:
                            errors.extend(self._validate_query_parameter(parameter, rule, method, path))
                        else:
                            errors.append(
                                f"Paramètre de requête '{param_name}' est manquant dans {method_upper} {path}. "
                                f"Il devrait être comme suit :\n"
                                f"  - name: '{param_name}'\n"
                                f"    type: '{rule.get('type')}'\n"
                                f"    required: {rule.get('required')}\n"
                                f"    description: '{rule.get('description')}'\n"
                                f"    example: '{rule.get('value')}'\n"
                            )
        return errors

    def _find_query_parameter(self, param_name, parameters):
        """
        Trouve un paramètre de requête spécifique dans les paramètres.

        :param param_name: Nom du paramètre de requête à rechercher.
        :param parameters: Liste des paramètres pour une méthode donnée.
        :return: Le dictionnaire du paramètre trouvé ou None.
        """
        for param in parameters:
            if param.get("in") == "query" and param.get("name").lower() == param_name.lower():
                return param
        return None

    def _validate_query_parameter(self, parameter, rule, method, path):
        """
        Valide un paramètre de requête en fonction d'une règle spécifique.

        :param parameter: Le dictionnaire du paramètre à valider.
        :param rule: La règle de validation pour ce paramètre.
        :param method: La méthode HTTP pour laquelle ce paramètre est utilisé.
        :param path: Le chemin d'API pour lequel ce paramètre est utilisé.
        :return: Une liste d'erreurs si la validation échoue.
        """
        errors = []
        param_name = rule["name"]

        def format_rule():
            return (
                f"Le paramètre '{param_name}' dans {method.upper()} {path} devrait être :\n"
                f"  - name: '{param_name}'\n"
                f"    type: '{rule.get('type')}'\n"
                f"    required: {rule.get('required')}\n"
                f"    description: '{rule.get('description')}'\n"
                f"    example: '{rule.get('value')}'\n"
            )

        if rule.get("type") and parameter.get("schema", {}).get("type") != rule["type"]:
            errors.append(
                f"Le type du paramètre '{param_name}' dans {method.upper()} {path} est '{parameter.get('schema', {}).get('type')}', "
                f"mais il devrait être '{rule['type']}'.\n{format_rule()}"
            )

        if rule.get("value") and parameter.get("example") != rule["value"]:
            errors.append(
                f"L'exemple du paramètre '{param_name}' dans {method.upper()} {path} est '{parameter.get('example')}', "
                f"mais il devrait être '{rule['value']}'.\n{format_rule()}"
            )

        if rule.get("description") and parameter.get("description") != rule["description"]:
            errors.append(
                f"La description du paramètre '{param_name}' dans {method.upper()} {path} est '{parameter.get('description')}', "
                f"mais il devrait être '{rule['description']}'.\n{format_rule()}"
            )

        return errors
