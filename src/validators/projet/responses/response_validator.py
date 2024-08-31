from ..base_validator import BaseValidator

class ResponseValidator(BaseValidator):
    """
    Valide les réponses définies dans le Swagger en fonction des règles spécifiques pour chaque méthode HTTP,
    en tenant compte des références ($ref) dans les schémas.
    """

    def __init__(self, swagger_dict, swagger_text, rules):
        """
        Initialise le validateur avec les règles de validation des réponses pour chaque méthode HTTP.
        
        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        :param rules: Règles spécifiques pour chaque méthode HTTP.
        """
        super().__init__(swagger_dict, swagger_text)
        self.rules = rules

    def resolve_reference(self, ref):
        """
        Résout une référence $ref dans le Swagger.

        :param ref: Le chemin de la référence sous la forme '#/components/schemas/SchemaName'.
        :return: Le schéma référencé sous forme de dictionnaire.
        """
        ref_path = ref.lstrip('#/').split('/')
        resolved = self.swagger_dict
        for part in ref_path:
            resolved = resolved.get(part, {})
        return resolved

    def validate_responses(self):
        """
        Valide les réponses dans le Swagger en fonction des règles spécifiées pour chaque méthode HTTP.
        
        :return: Une liste d'erreurs trouvées lors de la validation des réponses.
        """
        errors = []
        paths = self.swagger_dict.get('paths', {})

        for path, path_data in paths.items():
            for method, method_data in path_data.items():
                method_upper = method.upper()
                if method_upper in self.rules:
                    for expected_response in self.rules[method_upper].get("responses", []):
                        response_code = str(expected_response["response_code"])
                        actual_response = method_data.get('responses', {}).get(response_code, {})
                        if not actual_response:
                            errors.append(f"La réponse pour le code '{response_code}' est manquante dans {method_upper} {path}.")
                        else:
                            content_type = next(iter(actual_response.get("content", {}).keys()), None)
                            actual_schema = actual_response.get("content", {}).get(content_type, {}).get("schema", {})
                            expected_schema = expected_response["format"]

                            if "$ref" in actual_schema:
                                actual_schema = self.resolve_reference(actual_schema["$ref"])

                            errors.extend(self._validate_response_schema(actual_schema, expected_schema, response_code, method, path))
        return errors

    def _validate_response_schema(self, actual_schema, expected_schema, response_code, method, path):
        """
        Valide le schéma d'une réponse en fonction d'un schéma attendu.

        :param actual_schema: Le schéma réel extrait de la réponse Swagger.
        :param expected_schema: Le schéma attendu selon les règles.
        :param response_code: Le code de la réponse (200, 404, etc.).
        :param method: La méthode HTTP pour laquelle cette réponse est utilisée.
        :param path: Le chemin d'API pour lequel cette réponse est utilisée.
        :return: Une liste d'erreurs si la validation échoue.
        """
        errors = []

        def format_rule():
            return (
                f"Le schéma de la réponse pour le code '{response_code}' dans {method.upper()} {path} devrait être :\n"
                f"{expected_schema}\n"
            )

        if expected_schema.get("type") and actual_schema.get("type") != expected_schema["type"]:
            errors.append(
                f"Le type de la réponse pour le code '{response_code}' dans {method.upper()} {path} est '{actual_schema.get('type')}', "
                f"mais il devrait être '{expected_schema['type']}'.\n{format_rule()}"
            )

        if expected_schema.get("properties"):
            for prop, prop_expected_schema in expected_schema.get("properties", {}).items():
                if prop not in actual_schema.get("properties", {}):
                    errors.append(f"Le champ '{prop}' est manquant dans la réponse pour le code '{response_code}' dans {method.upper()} {path}.\n{format_rule()}")
                else:
                    actual_prop_schema = actual_schema.get("properties", {}).get(prop)
                    if "$ref" in actual_prop_schema:
                        actual_prop_schema = self.resolve_reference(actual_prop_schema["$ref"])

                    if prop_expected_schema.get("type") and actual_prop_schema.get("type") != prop_expected_schema["type"]:
                        errors.append(
                            f"Le type du champ '{prop}' dans la réponse pour le code '{response_code}' dans {method.upper()} {path} est '{actual_prop_schema.get('type')}', "
                            f"mais il devrait être '{prop_expected_schema['type']}'.\n{format_rule()}"
                        )

        if expected_schema.get("items"):
            actual_items_schema = actual_schema.get("items", {})
            if "$ref" in actual_items_schema:
                actual_items_schema = self.resolve_reference(actual_items_schema["$ref"])

            errors.extend(self._validate_response_schema(actual_items_schema, expected_schema["items"], response_code, method, path))

        return errors
