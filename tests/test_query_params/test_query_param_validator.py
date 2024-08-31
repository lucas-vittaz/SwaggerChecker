import pytest
from src.validators.projet.query_params.query_param_validator import QueryParamValidator

@pytest.fixture
def rules():
    return {
        "GET": {
            "query_parameters": [
                {
                    "name": "toto",
                    "description": "Numéro de toto",
                    "required": True,
                    "type": "integer",
                    "format": "int32",
                    "value": 0
                },
                {
                    "name": "exampleParam",
                    "description": "Exemple de paramètre",
                    "required": True,
                    "type": "string",
                    "value": "example"
                }
            ]
        }
    }

@pytest.fixture
def swagger_valid_query_params():
    return {
        "paths": {
            "/example": {
                "get": {
                    "parameters": [
                        {
                            "name": "toto",
                            "in": "query",
                            "description": "Numéro de toto",
                            "required": True,
                            "schema": {
                                "type": "integer",
                                "format": "int32"
                            },
                            "example": 0
                        },
                        {
                            "name": "exampleParam",
                            "in": "query",
                            "description": "Exemple de paramètre",
                            "required": True,
                            "schema": {
                                "type": "string"
                            },
                            "example": "example"
                        }
                    ]
                }
            }
        }
    }

@pytest.fixture
def swagger_incorrect_query_params():
    return {
        "paths": {
            "/example": {
                "get": {
                    "parameters": [
                        {
                            "name": "toto",
                            "in": "query",
                            "description": "Mauvaise description",
                            "required": True,
                            "schema": {
                                "type": "string"  # Mauvais type
                            },
                            "example": "wrong_example"  # Mauvais exemple
                        },
                        {
                            "name": "exampleParam",
                            "in": "query",
                            "description": "Mauvaise description",
                            "required": False,  # Mauvais required
                            "schema": {
                                "type": "integer"  # Mauvais type
                            },
                            "example": 123  # Mauvais exemple
                        }
                    ]
                }
            }
        }
    }

@pytest.fixture
def swagger_missing_query_params():
    return {
        "paths": {
            "/example": {
                "get": {
                    "parameters": []
                }
            }
        }
    }

def test_valid_query_params(swagger_valid_query_params, rules):
    validator = QueryParamValidator(swagger_valid_query_params, "", rules)
    errors = validator.validate_query_parameters()
    assert not errors, "Aucune erreur ne devrait être trouvée pour des paramètres de requête valides"

def test_incorrect_query_params(swagger_incorrect_query_params, rules):
    validator = QueryParamValidator(swagger_incorrect_query_params, "", rules)
    errors = validator.validate_query_parameters()
    assert errors, "Des erreurs devraient être trouvées pour les paramètres de requête incorrects"

def test_missing_query_params(swagger_missing_query_params, rules):
    validator = QueryParamValidator(swagger_missing_query_params, "", rules)
    errors = validator.validate_query_parameters()
    assert errors, "Des erreurs devraient être trouvées pour les paramètres de requête manquants"
