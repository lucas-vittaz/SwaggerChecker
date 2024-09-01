from ..base_validator import BaseValidator

class ReservedHeaderValidator(BaseValidator):
    """
    Valide les en-têtes définis dans le Swagger pour s'assurer qu'ils ne contiennent pas de mots réservés.
    """

    def __init__(self, swagger_dict, swagger_text, reserved_headers):
        """
        Initialise le validateur d'en-têtes avec les en-têtes réservés.
        
        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        :param reserved_headers: Liste des en-têtes réservés à valider.
        """
        super().__init__(swagger_dict, swagger_text)
        self.reserved_headers = reserved_headers

    def validate_reserved_headers(self):
        """
        Vérifie que les en-têtes définis dans chaque chemin du Swagger ne contiennent pas de mots réservés.
        
        :return: Une liste d'erreurs trouvées lors de la validation des en-têtes réservés.
        """
        errors = []
        paths = self.swagger_dict.get('paths', {})
        for path_data in paths.values():
            for method_data in path_data.values():
                for param in method_data.get('parameters', []):
                    if param.get('in') == 'header':
                        header_name = param.get('name')
                        for reserved in self.reserved_headers:
                            if reserved.lower() == header_name.lower():
                                line_number = self._find_line_number(header_name)
                                errors.append(f"Header '{header_name}' contient un mot réservé '{reserved}' (ligne {line_number})")
        return errors
