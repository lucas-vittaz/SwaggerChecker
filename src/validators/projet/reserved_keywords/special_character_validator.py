import re

from ..base_validator import BaseValidator

class SpecialCharacterValidator(BaseValidator):
    """
    Valide que les valeurs dans le Swagger ne contiennent pas de caractères spéciaux non autorisés.
    """

    def __init__(self, swagger_dict, swagger_text, special_characters):
        """
        Initialise le validateur de caractères spéciaux.
        
        :param swagger_dict: Dictionnaire contenant la représentation du fichier Swagger.
        :param swagger_text: Chaîne de caractères contenant le texte brut du fichier Swagger.
        :param special_characters: Liste des caractères spéciaux à valider.
        """
        super().__init__(swagger_dict, swagger_text)
        self.special_characters = special_characters
        self.special_characters_pattern = re.compile(f"[{''.join(re.escape(char) for char in special_characters)}]")

    def validate_all_values(self):
        """
        Valide toutes les valeurs dans le dictionnaire Swagger pour vérifier qu'elles ne contiennent pas de caractères spéciaux.
        
        :return: Une liste d'erreurs si des caractères spéciaux sont trouvés, sinon une liste vide.
        """
        errors = []
        self._check_dict(self.swagger_dict, errors)
        return errors

    def _check_dict(self, current_dict, errors, path="root"):
        """
        Parcourt de manière récursive un dictionnaire pour valider ses valeurs.

        :param current_dict: Le dictionnaire actuel à vérifier.
        :param errors: Liste d'erreurs accumulées.
        :param path: Chemin actuel dans la structure du dictionnaire.
        """
        for key, value in current_dict.items():
            new_path = f"{path}.{key}"
            if isinstance(value, dict):
                self._check_dict(value, errors, new_path)
            elif isinstance(value, list):
                self._check_list(value, errors, new_path)
            else:
                self._check_value(key, value, errors, new_path)

    def _check_list(self, current_list, errors, path):
        """
        Parcourt une liste pour valider ses valeurs.

        :param current_list: La liste actuelle à vérifier.
        :param errors: Liste d'erreurs accumulées.
        :param path: Chemin actuel dans la structure du dictionnaire.
        """
        for index, item in enumerate(current_list):
            new_path = f"{path}[{index}]"
            if isinstance(item, dict):
                self._check_dict(item, errors, new_path)
            elif isinstance(item, list):
                self._check_list(item, errors, new_path)
            else:
                self._check_value(f"[{index}]", item, errors, new_path)

    def _check_value(self, key, value, errors, path):
        """
        Valide une valeur individuelle pour vérifier qu'elle ne contient pas de caractères spéciaux.

        :param key: Le nom du champ à vérifier.
        :param value: La valeur à vérifier.
        :param errors: Liste d'erreurs accumulées.
        :param path: Chemin actuel dans la structure du dictionnaire.
        """
        if isinstance(value, str) and self.special_characters_pattern.search(value):
            errors.append(f"La valeur '{value}' sous le chemin '{path}' contient des caractères spéciaux non autorisés.")

