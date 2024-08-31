import pytest
from src.validators.projet.headers.header_validator import HeaderValidator

@pytest.fixture
def swagger_missing_headers():
    return {
        "paths": {
            "/example": {
                "get": {"parameters": []},
                "post": {"parameters": []},
                "put": {"parameters": []},
                "delete": {"parameters": []},
            }
        }
    }

@pytest.fixture
def swagger_incorrect_headers():
    return {
        "paths": {
            "/example": {
                "get": {
                    "parameters": [
                        {
                            "name": "Content-Type",
                            "in": "header",
                            "schema": {"type": "integer", "example": "wrong_example"},
                            "description": "Mauvaise description"
                        }
                    ]
                },
                "post": {
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "schema": {"type": "integer", "example": "wrong_example"},
                            "description": "Mauvaise description"
                        }
                    ]
                },
                "put": {
                    "parameters": [
                        {
                            "name": "Content-Length",
                            "in": "header",
                            "schema": {"type": "string"},
                            "description": "Mauvais type pour PUT"
                        }
                    ]
                },
                "delete": {
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "schema": {"type": "string", "example": "Bearer token"},
                            "description": "Mauvaise description"
                        }
                    ]
                }
            }
        }
    }

@pytest.fixture
def swagger_valid_headers():
    return {
        "paths": {
            "/example": {
                "get": {
                    "parameters": [
                        {
                            "name": "Content-Type",
                            "in": "header",
                            "schema": {"type": "string"},
                            "description": "Type de contenu pour GET",
                            "required": True,
                            "example": "application/json"
                        }
                    ]
                },
                "post": {
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "schema": {"type": "string"},
                            "description": "Jeton d'authentification pour POST",
                            "required": True,
                            "example": "Bearer token"
                        }
                    ]
                },
                "put": {
                    "parameters": [
                        {
                            "name": "Content-Length",
                            "in": "header",
                            "schema": {"type": "integer"},
                            "description": "La longueur du contenu pour PUT",
                            "required": True,
                            "example": 123
                        }
                    ]
                },
                "delete": {
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "schema": {"type": "string"},
                            "description": "Jeton d'authentification pour DELETE",
                            "required": True,
                            "example": "Bearer token"
                        }
                    ]
                }
            }
        }
    }

@pytest.fixture
def rules():
    return {
        "GET": {
            "headers": [
                {
                    "name": "Content-Type",
                    "type": "string",
                    "required": True,
                    "description": "Type de contenu pour GET",
                    "x-example": "application/json"
                }
            ]
        },
        "POST": {
            "headers": [
                {
                    "name": "Authorization",
                    "type": "string",
                    "required": True,
                    "description": "Jeton d'authentification pour POST",
                    "x-example": "Bearer token"
                }
            ]
        },
        "PUT": {
            "headers": [
                {
                    "name": "Content-Length",
                    "type": "integer",
                    "required": True,
                    "description": "La longueur du contenu pour PUT",
                    "x-example": 123
                }
            ]
        },
        "DELETE": {
            "headers": [
                {
                    "name": "Authorization",
                    "type": "string",
                    "required": True,
                    "description": "Jeton d'authentification pour DELETE",
                    "x-example": "Bearer token"
                }
            ]
        }
    }

def test_missing_headers(swagger_missing_headers, rules):
    validator = HeaderValidator(swagger_missing_headers, "", rules)
    errors = validator.validate_headers()
    assert errors, "Des erreurs devraient être trouvées pour les en-têtes manquants"

def test_incorrect_headers(swagger_incorrect_headers, rules):
    validator = HeaderValidator(swagger_incorrect_headers, "", rules)
    errors = validator.validate_headers()
    assert errors, "Des erreurs devraient être trouvées pour les en-têtes incorrects"

def test_valid_headers(swagger_valid_headers, rules):
    validator = HeaderValidator(swagger_valid_headers, "", rules)
    errors = validator.validate_headers()
    assert not errors, "Aucune erreur ne devrait être trouvée pour des en-têtes valides"
