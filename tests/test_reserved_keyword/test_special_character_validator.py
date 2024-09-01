import pytest
import json

from src.validators.projet.reserved_keywords.special_character_validator import SpecialCharacterValidator

@pytest.fixture
def special_characters():
    with open('config/projet_validation_rules.json', 'r') as f:
        config = json.load(f)
    return config["special_characters"]

@pytest.fixture
def swagger_dict_passant():
    return {
        "info": {
            "title": "Valid API",
            "version": "1.0.0",
            "description": "This description is clean."
        },
        "paths": {
            "/api/v1/pet": {
                "get": {
                    "summary": "Get pet details",
                    "responses": {
                        "200": {
                            "description": "successful operation"
                        }
                    }
                }
            }
        }
    }

@pytest.fixture
def swagger_dict_non_passant():
    return {
        "info": {
            "title": "Invalid~ API",
            "version": "1.0.0",
            "description": "This description contains a ~ special character."
        },
        "paths": {
            "/api/v1/pet": {
                "get": {
                    "summary": "Get pet details",
                    "responses": {
                        "200": {
                            "description": "successful operation"
                        }
                    }
                }
            },
            "/api/v1/user": {
                "get": {
                    "summary": "Get user details~",
                    "responses": {
                        "200": {
                            "description": "successful operation"
                        }
                    }
                }
            }
        }
    }

@pytest.fixture
def swagger_text():
    return """
    info:
        title: "Valid API"
        version: "1.0.0"
        description: "This description is clean."
    paths:
        /api/v1/pet:
            get:
                summary: "Get pet details"
                responses:
                    200:
                        description: "successful operation"
    """

def test_validate_special_characters_passant(swagger_dict_passant, swagger_text, special_characters):
    validator = SpecialCharacterValidator(swagger_dict_passant, swagger_text, special_characters)
    errors = validator.validate_all_values()
    assert len(errors) == 0, f"Des erreurs ont été trouvées dans un cas passant: {errors}"

def test_validate_special_characters_non_passant(swagger_dict_non_passant, swagger_text, special_characters):
    validator = SpecialCharacterValidator(swagger_dict_non_passant, swagger_text, special_characters)
    errors = validator.validate_all_values()
    assert len(errors) == 3, f"Le nombre d'erreurs devrait être 3, mais est {len(errors)}. Erreurs: {errors}"
    assert "La valeur 'Invalid~ API' sous le chemin 'root.info.title' contient des caractères spéciaux non autorisés." in errors[0]
    assert "La valeur 'This description contains a ~ special character.' sous le chemin 'root.info.description' contient des caractères spéciaux non autorisés." in errors[1]
    assert "La valeur 'Get user details~' sous le chemin 'root.paths./api/v1/user.get.summary' contient des caractères spéciaux non autorisés." in errors[2]
