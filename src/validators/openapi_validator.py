from openapi_spec_validator import openapi_v2_spec_validator, openapi_v3_spec_validator

class OpenAPIValidator:
    """
    Classe pour valider un fichier Swagger/OpenAPI contre les spécifications OpenAPI.

    Attributes:
        swagger_dict (dict): Le dictionnaire représentant le fichier Swagger/OpenAPI.
        swagger_text (list): Liste des lignes du fichier Swagger/OpenAPI en texte brut.
    """

    def __init__(self, swagger_dict, swagger_text):
        """
        Initialise l'objet OpenAPIValidator avec le dictionnaire Swagger et le texte brut.

        Args:
            swagger_dict (dict): Le dictionnaire représentant le fichier Swagger/OpenAPI.
            swagger_text (str): Le texte brut du fichier Swagger/OpenAPI.
        """
        self.swagger_dict = swagger_dict
        self.swagger_text = swagger_text.splitlines()

    def validate(self):
        """
        Valide le fichier Swagger/OpenAPI contre les spécifications OpenAPI.

        Utilise le validateur approprié en fonction de la version de Swagger/OpenAPI.

        Returns:
            tuple: Un booléen indiquant si la validation a réussi, et un message d'erreur ou de succès.
        """
        errors = []
        try:
            if 'swagger' in self.swagger_dict:
                validator = openapi_v2_spec_validator
            elif 'openapi' in self.swagger_dict:
                validator = openapi_v3_spec_validator
            else:
                raise Exception("Version Swagger/OpenAPI non spécifiée.")

            for error in validator.iter_errors(self.swagger_dict):
                error_message = self._extract_error_line(str(error))
                errors.append(error_message)

            if errors:
                return False, "\n".join(errors)
            else:
                return True, "Le swagger respecte la norme OpenAPI."
        except Exception as e:
            return False, f"Erreur lors de la validation OpenAPI: {str(e)}"

    def _extract_error_line(self, error_message):
        """
        Extrait la ligne du fichier Swagger correspondant à l'erreur.

        Args:
            error_message (str): Le message d'erreur généré par le validateur.

        Returns:
            str: Une chaîne indiquant la ligne de l'erreur ou un message d'erreur.
        """
        for index, line in enumerate(self.swagger_text, start=1):
            if error_message.split(":")[0] in line:
                return f"Ligne {index}: {error_message}"
        return f"Erreur: {error_message}"
