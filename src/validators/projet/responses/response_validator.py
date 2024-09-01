from ..base_validator import BaseValidator

class ResponseValidator(BaseValidator):
    def __init__(self, swagger_dict, swagger_text, rules):
        super().__init__(swagger_dict, swagger_text)
        self.rules = rules

    def validate_responses(self):
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

                            errors.extend(self._validate_response_schema(actual_schema, expected_schema, response_code, method, path))
        return errors

    def _validate_response_schema(self, actual_schema, expected_schema, response_code, method, path):
        errors = []

        def format_rule():
            return (
                f"Le schéma de la réponse pour le code '{response_code}' dans {method.upper()} {path} devrait être :\n"
                f"{expected_schema}\n"
            )

        actual_type = actual_schema.get("type")
        expected_type = expected_schema.get("type")

        if expected_type and actual_type != expected_type:
            # Ne pas signaler d'erreur si le schéma attendu est vide
            if not actual_schema and expected_schema == {}:
                return errors
            errors.append(
                f"Le type de la réponse pour le code '{response_code}' dans {method.upper()} {path} est '{actual_type}', "
                f"mais il devrait être '{expected_type}'.\n{format_rule()}"
            )

        if expected_schema.get("properties"):
            for prop, prop_expected_schema in expected_schema.get("properties", {}).items():
                actual_prop_schema = actual_schema.get("properties", {}).get(prop)
                if not actual_prop_schema:
                    errors.append(f"Le champ '{prop}' est manquant dans la réponse pour le code '{response_code}' dans {method.upper()} {path}.\n{format_rule()}")
                else:
                    if prop_expected_schema.get("type") and actual_prop_schema.get("type") != prop_expected_schema["type"]:
                        errors.append(
                            f"Le type du champ '{prop}' dans la réponse pour le code '{response_code}' dans {method.upper()} {path} est '{actual_prop_schema.get('type')}', "
                            f"mais il devrait être '{prop_expected_schema['type']}'.\n{format_rule()}"
                        )

        if expected_schema.get("items"):
            actual_items_schema = actual_schema.get("items", {})

            errors.extend(self._validate_response_schema(actual_items_schema, expected_schema["items"], response_code, method, path))

        return errors
