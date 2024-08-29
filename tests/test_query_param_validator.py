import pytest
import json
from src.validators.projet.query_param_validator import QueryParamValidator

@pytest.fixture
def reserved_query_parameters():
    with open('config/projet_validation_rules.json', 'r') as f:
        config = json.load(f)
    return config["reserved_query_parameters"]

@pytest.fixture
def swagger_dict_passant():
    return {
        "paths": {
            "/api/v1/pet": {
                "get": {
                    "parameters": [
                        {
                            "name": "status",
                            "in": "query",
                            "required": False,
                            "type": "string"
                        }
                    ]
                }
            },
            "/api/v1/user": {
                "get": {
                    "parameters": [
                        {
                            "name": "role",
                            "in": "query",
                            "required": False,
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
                            "name": "john",
                            "in": "query",
                            "required": False,
                            "type": "string"
                        }
                    ]
                }
            },
            "/api/v1/user": {
                "get": {
                    "parameters": [
                        {
                            "name": "doe",
                            "in": "query",
                            "required": False,
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
                - name: john
                  in: query
                  required: false
                  type: string
    /api/v1/user:
        get:
            parameters:
                - name: doe
                  in: query
                  required: false
                  type: string
    """

def test_validate_reserved_query_parameters_passant(swagger_dict_passant, swagger_text, reserved_query_parameters):
    validator = QueryParamValidator(swagger_dict_passant, swagger_text, reserved_query_parameters)
    errors = validator.validate_reserved_query_parameters()
    assert len(errors) == 0, f"Des erreurs ont été trouvées dans un cas passant: {errors}"

def test_validate_reserved_query_parameters_non_passant(swagger_dict_non_passant, swagger_text, reserved_query_parameters):
    validator = QueryParamValidator(swagger_dict_non_passant, swagger_text, reserved_query_parameters)
    errors = validator.validate_reserved_query_parameters()
    assert len(errors) == 2, f"Le nombre d'erreurs devrait être 2, mais est {len(errors)}. Erreurs: {errors}"
    assert "Paramètre de requête 'john' contient un mot réservé 'john'" in errors[0]
    assert "Paramètre de requête 'doe' contient un mot réservé 'doe'" in errors[1]
