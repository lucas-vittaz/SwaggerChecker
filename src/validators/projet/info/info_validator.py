from ..base_validator import BaseValidator
import re

class InfoValidator(BaseValidator):
    """
    Valide les informations générales du Swagger telles que le titre, la version, la description et le basePath.
    """

    def validate_title(self):
        """
        Vérifie que le Swagger possède un titre.
        
        :return: Une liste d'erreurs trouvées lors de la validation du titre.
        """
        errors = []
        title = self.swagger_dict.get('info', {}).get('title', '')
        if not title:
            errors.append("Le Swagger ne contient pas de titre dans la section 'info'.")
        return errors

    def validate_version(self):
        """
        Vérifie que la version du Swagger commence par 'v' suivi d'un chiffre.
        
        :return: Une liste d'erreurs trouvées lors de la validation de la version.
        """
        errors = []
        version = self.swagger_dict.get('info', {}).get('version', '')
        if not re.match(r'^v\d+', version):
            errors.append("La version du Swagger doit commencer par 'v' suivi d'un chiffre.")
        return errors

    def validate_description(self):
        """
        Vérifie que le Swagger possède une description non vide.
        
        :return: Une liste d'erreurs trouvées lors de la validation de la description.
        """
        errors = []
        description = self.swagger_dict.get('info', {}).get('description', '')
        if not description or description.strip() == '':
            errors.append("Le Swagger contient une description vide ou absente dans la section 'info'.")
        return errors

    def validate_basepath(self):
        """
        Vérifie que le basePath du Swagger est correctement formaté comme 'nom_de_lapi/nom_de_version'.
        
        :return: Une liste d'erreurs trouvées lors de la validation du basePath.
        """
        errors = []
        base_path = self.swagger_dict.get('basePath', '')
        info = self.swagger_dict.get('info', {})
        title = info.get('title', '')
        version = info.get('version', '')
        expected_base_path = f"/{title}/{version}"
        if base_path != expected_base_path:
            errors.append(f"Le `basePath` est incorrect : attendu '{expected_base_path}', trouvé '{base_path}'.")
        return errors
