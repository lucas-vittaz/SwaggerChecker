from ..base_validator import BaseValidator

class ReservedPathValidator(BaseValidator):
    """
    Valide les chemins définis dans le Swagger pour s'assurer qu'ils ne contiennent pas de mots réservés.
    """

    def __init__(self, swagger_dict, swagger_text, reserved_paths):
        """
        Initialise le validateur de chemins avec les chemins réservés.
        
        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        :param reserved_paths: Liste des chemins réservés à valider.
        """
        super().__init__(swagger_dict, swagger_text)
        self.reserved_paths = reserved_paths

    def validate_reserved_paths(self):
        """
        Vérifie que les chemins définis dans le Swagger ne contiennent pas de mots réservés.
        
        :return: Une liste d'erreurs trouvées lors de la validation des chemins réservés.
        """
        errors = []
        for path in self.swagger_dict.get('paths', {}).keys():
            for reserved in self.reserved_paths:
                if reserved in path.split('/'):
                    line_number = self._find_line_number(path)
                    errors.append(f"Le chemin '{path}' contient un mot réservé '{reserved}' (ligne {line_number})")
        return errors
