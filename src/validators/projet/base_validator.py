class BaseValidator:
    """
    Classe de base pour les validateurs spécifiques. Contient des utilitaires communs utilisés par les validateurs.
    """

    def __init__(self, swagger_dict, swagger_text):
        """
        Initialise le validateur de base avec le dictionnaire Swagger et le texte Swagger.
        
        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        """
        self.swagger_dict = swagger_dict
        self.swagger_text = swagger_text.splitlines()

    def _find_line_number(self, keyword):
        """
        Recherche un mot-clé spécifique dans le texte brut du Swagger et retourne le numéro de la ligne où il apparaît.
        
        :param keyword: Mot-clé à rechercher dans le texte du Swagger.
        :return: Le numéro de la ligne où le mot-clé a été trouvé, ou "inconnue" s'il n'a pas été trouvé.
        """
        for index, line in enumerate(self.swagger_text, start=1):
            if keyword in line:
                return index
        return "inconnue"
