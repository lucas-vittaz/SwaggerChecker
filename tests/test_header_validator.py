import pytest
import json
from src.validators.projet.header_validator import HeaderValidator

@pytest.fixture
def reserved_headers():
    with open('config/projet_validation_rules.json', 'r') as f:
        config = json.load(f)
    return config["reserved_headers"]

@pytest.fixture
def swagger_dict_passant():
    return {
        "paths": {
            "/api/v1/pet": {
                "get": {
                    "parameters": [
                        {
                            "name": "X-Request-ID",
                            "in": "header",
                            "required": True,
                            "type": "string"
                        }
                    ]
                }
            },
            "/api/v1/user": {
                "get": {
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "required": True,
                            "type": "string"
                        }
                    ]
                }
            }
        }
    }

@pytest.fixture
def swagger_dict_non_passant():
    return {
        "paths": {
            "/api/v1/pet": {
                "get": {
                    "parameters": [
                        {
                            "name": "toto",
                            "in": "header",
                            "required": True,
                            "type": "string"
                        }
                    ]
                }
            },
            "/api/v1/user": {
                "get": {
                    "parameters": [
                        {
                            "name": "tata",
                            "in": "header",
                            "required": True,
                            "type": "string"
                        }
                    ]
                }
            }
        }
    }

@pytest.fixture
def swagger_text():
    return """
    /api/v1/pet:
        get:
            parameters:
                - name: X-Request-ID
                  in: header
                  required: true
                  type: string
    /api/v1/user:
        get:
            parameters:
                - name: Authorization
                  in: header
                  required: true
                  type: string
    """

def test_validate_reserved_headers_passant(swagger_dict_passant, swagger_text, reserved_headers):
    validator = HeaderValidator(swagger_dict_passant, swagger_text, reserved_headers)
    errors = validator.validate_reserved_headers()
    assert len(errors) == 0, f"Des erreurs ont été trouvées dans un cas passant: {errors}"

def test_validate_reserved_headers_non_passant(swagger_dict_non_passant, swagger_text, reserved_headers):
    validator = HeaderValidator(swagger_dict_non_passant, swagger_text, reserved_headers)
    errors = validator.validate_reserved_headers()
    assert len(errors) == 2, f"Le nombre d'erreurs devrait être 2, mais est {len(errors)}. Erreurs: {errors}"
    assert "Header 'toto' contient un mot réservé 'toto'" in errors[0]
    assert "Header 'tata' contient un mot réservé 'tata'" in errors[1]
