from ..base_validator import BaseValidator

class HeaderValidator(BaseValidator):
    """
    Valide les en-têtes définis dans le Swagger en fonction des règles spécifiques pour chaque méthode HTTP.
    """

    def __init__(self, swagger_dict, swagger_text, rules):
        """
        Initialise le validateur avec les règles de validation des en-têtes pour chaque méthode HTTP.
        
        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        :param rules: Règles spécifiques pour chaque méthode HTTP.
        """
        super().__init__(swagger_dict, swagger_text)
        self.rules = rules

    def validate_headers(self):
        """
        Valide les en-têtes dans le Swagger en fonction des règles spécifiées pour chaque méthode HTTP.
        
        :return: Une liste d'erreurs trouvées lors de la validation des en-têtes.
        """
        errors = []
        paths = self.swagger_dict.get('paths', {})

        for path, path_data in paths.items():
            for method, method_data in path_data.items():
                method_upper = method.upper()
                if method_upper in self.rules:
                    for rule in self.rules[method_upper].get("headers", []):
                        header_name = rule["name"]
                        parameter = self._find_header(header_name, method_data.get('parameters', []))
                        if parameter:
                            errors.extend(self._validate_header(parameter, rule, method, path))
                        else:
                            errors.append(
                                f"Header '{header_name}' est manquant dans {method_upper} {path}. "
                                f"Il devrait être comme suit :\n"
                                f"  - name: '{header_name}'\n"
                                f"    type: '{rule.get('type')}'\n"
                                f"    required: {rule.get('required')}\n"
                                f"    description: '{rule.get('description')}'\n"
                                f"    example: '{rule.get('x-example')}'\n"
                            )
        return errors

    def _find_header(self, header_name, parameters):
        """
        Trouve un en-tête spécifique dans les paramètres.

        :param header_name: Nom de l'en-tête à rechercher.
        :param parameters: Liste des paramètres pour une méthode donnée.
        :return: Le dictionnaire de l'en-tête trouvé ou None.
        """
        for param in parameters:
            if param.get("in") == "header" and param.get("name").lower() == header_name.lower():
                return param
        return None

    def _validate_header(self, parameter, rule, method, path):
        """
        Valide un en-tête en fonction d'une règle spécifique.

        :param parameter: Le dictionnaire de l'en-tête à valider.
        :param rule: La règle de validation pour cet en-tête.
        :param method: La méthode HTTP pour laquelle cet en-tête est utilisé.
        :param path: Le chemin d'API pour lequel cet en-tête est utilisé.
        :return: Une liste d'erreurs si la validation échoue.
        """
        errors = []
        header_name = rule["name"]
        schema = parameter.get("schema", {})

        def format_rule():
            return (
                f"Le header '{header_name}' dans {method.upper()} {path} devrait être :\n"
                f"  - name: '{header_name}'\n"
                f"    type: '{rule.get('type')}'\n"
                f"    required: {rule.get('required')}\n"
                f"    description: '{rule.get('description')}'\n"
                f"    example: '{rule.get('x-example')}'\n"
            )

        example = schema.get("example")
        if example is None:
            example = parameter.get("example")

        if rule.get("type") and schema.get("type") != rule["type"]:
            errors.append(
                f"Le type du header '{header_name}' dans {method.upper()} {path} est '{schema.get('type')}', "
                f"mais il devrait être '{rule['type']}'.\n{format_rule()}"
            )

        if rule.get("x-example") and example != rule["x-example"]:
            errors.append(
                f"L'exemple du header '{header_name}' dans {method.upper()} {path} est '{example}', "
                f"mais il devrait être '{rule['x-example']}'.\n{format_rule()}"
            )

        if rule.get("description") and parameter.get("description") != rule["description"]:
            errors.append(
                f"La description du header '{header_name}' dans {method.upper()} {path} est '{parameter.get('description')}', "
                f"mais il devrait être '{rule['description']}'.\n{format_rule()}"
            )

        return errors
