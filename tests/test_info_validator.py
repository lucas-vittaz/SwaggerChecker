import pytest
from src.validators.projet.info_validator import InfoValidator

@pytest.fixture
def swagger_dict_valid():
    return {
        "info": {
            "title": "TestAPI",
            "version": "v1",
            "description": "Ceci est une API de test"
        },
        "basePath": "/TestAPI/v1"
    }

@pytest.fixture
def swagger_dict_invalid_title():
    return {
        "info": {
            "version": "v1",
            "description": "Ceci est une API de test"
        },
        "basePath": "/TestAPI/v1"
    }

@pytest.fixture
def swagger_dict_invalid_version():
    return {
        "info": {
            "title": "TestAPI",
            "version": "1.0",
            "description": "Ceci est une API de test"
        },
        "basePath": "/TestAPI/v1"
    }

@pytest.fixture
def swagger_dict_invalid_description():
    return {
        "info": {
            "title": "TestAPI",
            "version": "v1",
            "description": ""
        },
        "basePath": "/TestAPI/v1"
    }

@pytest.fixture
def swagger_dict_invalid_basepath():
    return {
        "info": {
            "title": "TestAPI",
            "version": "v1",
            "description": "Ceci est une API de test"
        },
        "basePath": "/WrongPath/v1"
    }

def test_validate_title_with_valid(swagger_dict_valid):
    validator = InfoValidator(swagger_dict_valid, "")
    errors = validator.validate_title()
    assert not errors, f"Errors found: {errors}"

def test_validate_title_with_invalid(swagger_dict_invalid_title):
    validator = InfoValidator(swagger_dict_invalid_title, "")
    errors = validator.validate_title()
    assert errors == ["Le Swagger ne contient pas de titre dans la section 'info'."]

def test_validate_version_with_valid(swagger_dict_valid):
    validator = InfoValidator(swagger_dict_valid, "")
    errors = validator.validate_version()
    assert not errors, f"Errors found: {errors}"

def test_validate_version_with_invalid(swagger_dict_invalid_version):
    validator = InfoValidator(swagger_dict_invalid_version, "")
    errors = validator.validate_version()
    assert errors == ["La version du Swagger doit commencer par 'v' suivi d'un chiffre."]

def test_validate_description_with_valid(swagger_dict_valid):
    validator = InfoValidator(swagger_dict_valid, "")
    errors = validator.validate_description()
    assert not errors, f"Errors found: {errors}"

def test_validate_description_with_invalid(swagger_dict_invalid_description):
    validator = InfoValidator(swagger_dict_invalid_description, "")
    errors = validator.validate_description()
    assert errors == ["Le Swagger contient une description vide ou absente dans la section 'info'."]

def test_validate_basepath_with_valid(swagger_dict_valid):
    validator = InfoValidator(swagger_dict_valid, "")
    errors = validator.validate_basepath()
    assert not errors, f"Errors found: {errors}"

def test_validate_basepath_with_invalid(swagger_dict_invalid_basepath):
    validator = InfoValidator(swagger_dict_invalid_basepath, "")
    errors = validator.validate_basepath()
    assert errors == ["Le `basePath` est incorrect : attendu '/TestAPI/v1', trouvé '/WrongPath/v1'."]
