from .base_validator import BaseValidator

class QueryParamValidator(BaseValidator):
    """
    Valide les paramètres de requête définis dans le Swagger pour s'assurer qu'ils ne contiennent pas de mots réservés.
    """

    def __init__(self, swagger_dict, swagger_text, reserved_query_parameters):
        """
        Initialise le validateur de paramètres de requête avec les paramètres réservés.
        
        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        :param reserved_query_parameters: Liste des paramètres de requête réservés à valider.
        """
        super().__init__(swagger_dict, swagger_text)
        self.reserved_query_parameters = reserved_query_parameters

    def validate_reserved_query_parameters(self):
        """
        Vérifie que les paramètres de requête définis dans chaque chemin du Swagger ne contiennent pas de mots réservés.
        
        :return: Une liste d'erreurs trouvées lors de la validation des paramètres de requête réservés.
        """
        errors = []
        paths = self.swagger_dict.get('paths', {})
        for path, path_data in paths.items():
            for method, method_data in path_data.items():
                for param in method_data.get('parameters', []):
                    if param.get('in') == 'query':
                        param_name = param.get('name')
                        for reserved in self.reserved_query_parameters:
                            if reserved.lower() == param_name.lower():
                                line_number = self._find_line_number(param_name)
                                errors.append(f"Paramètre de requête '{param_name}' contient un mot réservé '{reserved}' (ligne {line_number}) dans {method.upper()} {path}")
        return errors
