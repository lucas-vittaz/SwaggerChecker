import html
from ..base_validator import BaseValidator

class HeaderValidator(BaseValidator):
    def __init__(self, swagger_dict, swagger_text, rules):
        super().__init__(swagger_dict, swagger_text)
        self.rules = rules

    def validate_headers(self):
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
        for param in parameters:
            if param.get("in") == "header" and param.get("name").lower() == header_name.lower():
                return param
        return None

    def _validate_header(self, parameter, rule, method, path):
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

        # Normaliser les descriptions pour ignorer les différences d'espaces ou de retours à la ligne
        actual_description = html.unescape(parameter.get("description", "").strip())
        expected_description = html.unescape(rule.get("description", "").strip())

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

        if expected_description and actual_description != expected_description:
            errors.append(
                f"La description du header '{header_name}' dans {method.upper()} {path} est '{actual_description}', "
                f"mais il devrait être '{expected_description}'.\n{format_rule()}"
            )

        return errors
