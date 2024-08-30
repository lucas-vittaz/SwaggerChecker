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
def swagger_additional_headers():
    return {
        "paths": {
            "/example": {
                "get": {
                    "parameters": [
                        {
                            "name": "Extra-Header",
                            "in": "header",
                            "schema": {"type": "string"},
                            "description": "Un en-tête supplémentaire non requis",
                            "required": False,
                            "example": "extra-value"
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
    
    expected_errors = [
        "Header 'Content-Type' est manquant dans GET /example. Il devrait être comme suit :\n"
        "  - name: 'Content-Type'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Type de contenu pour GET'\n"
        "    example: 'application/json'\n",

        "Header 'Authorization' est manquant dans POST /example. Il devrait être comme suit :\n"
        "  - name: 'Authorization'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Jeton d'authentification pour POST'\n"
        "    example: 'Bearer token'\n",

        "Header 'Content-Length' est manquant dans PUT /example. Il devrait être comme suit :\n"
        "  - name: 'Content-Length'\n"
        "    type: 'integer'\n"
        "    required: True\n"
        "    description: 'La longueur du contenu pour PUT'\n"
        "    example: '123'\n",

        "Header 'Authorization' est manquant dans DELETE /example. Il devrait être comme suit :\n"
        "  - name: 'Authorization'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Jeton d'authentification pour DELETE'\n"
        "    example: 'Bearer token'\n"
    ]

    assert errors == expected_errors, f"Les erreurs ne correspondent pas aux attentes. Reçues : {errors}"

def test_incorrect_headers(swagger_incorrect_headers, rules):
    validator = HeaderValidator(swagger_incorrect_headers, "", rules)
    errors = validator.validate_headers()
    
    expected_errors = [
        "Le type du header 'Content-Type' dans GET /example est 'integer', mais il devrait être 'string'.\n"
        "Le header 'Content-Type' dans GET /example devrait être :\n"
        "  - name: 'Content-Type'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Type de contenu pour GET'\n"
        "    example: 'application/json'\n",

        "L'exemple du header 'Content-Type' dans GET /example est 'wrong_example', mais il devrait être 'application/json'.\n"
        "Le header 'Content-Type' dans GET /example devrait être :\n"
        "  - name: 'Content-Type'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Type de contenu pour GET'\n"
        "    example: 'application/json'\n",

        "La description du header 'Content-Type' dans GET /example est 'Mauvaise description', mais il devrait être 'Type de contenu pour GET'.\n"
        "Le header 'Content-Type' dans GET /example devrait être :\n"
        "  - name: 'Content-Type'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Type de contenu pour GET'\n"
        "    example: 'application/json'\n",

        "Le type du header 'Authorization' dans POST /example est 'integer', mais il devrait être 'string'.\n"
        "Le header 'Authorization' dans POST /example devrait être :\n"
        "  - name: 'Authorization'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Jeton d'authentification pour POST'\n"
        "    example: 'Bearer token'\n",

        "L'exemple du header 'Authorization' dans POST /example est 'wrong_example', mais il devrait être 'Bearer token'.\n"
        "Le header 'Authorization' dans POST /example devrait être :\n"
        "  - name: 'Authorization'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Jeton d'authentification pour POST'\n"
        "    example: 'Bearer token'\n",

        "La description du header 'Authorization' dans POST /example est 'Mauvaise description', mais il devrait être 'Jeton d'authentification pour POST'.\n"
        "Le header 'Authorization' dans POST /example devrait être :\n"
        "  - name: 'Authorization'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Jeton d'authentification pour POST'\n"
        "    example: 'Bearer token'\n",

        "Le type du header 'Content-Length' dans PUT /example est 'string', mais il devrait être 'integer'.\n"
        "Le header 'Content-Length' dans PUT /example devrait être :\n"
        "  - name: 'Content-Length'\n"
        "    type: 'integer'\n"
        "    required: True\n"
        "    description: 'La longueur du contenu pour PUT'\n"
        "    example: '123'\n",

        "L'exemple du header 'Content-Length' dans PUT /example est '', mais il devrait être '123'.\n"
        "Le header 'Content-Length' dans PUT /example devrait être :\n"
        "  - name: 'Content-Length'\n"
        "    type: 'integer'\n"
        "    required: True\n"
        "    description: 'La longueur du contenu pour PUT'\n"
        "    example: '123'\n",

        "La description du header 'Content-Length' dans PUT /example est 'Mauvais type pour PUT', mais il devrait être 'La longueur du contenu pour PUT'.\n"
        "Le header 'Content-Length' dans PUT /example devrait être :\n"
        "  - name: 'Content-Length'\n"
        "    type: 'integer'\n"
        "    required: True\n"
        "    description: 'La longueur du contenu pour PUT'\n"
        "    example: '123'\n",

        "La description du header 'Authorization' dans DELETE /example est 'Mauvaise description', mais il devrait être 'Jeton d'authentification pour DELETE'.\n"
        "Le header 'Authorization' dans DELETE /example devrait être :\n"
        "  - name: 'Authorization'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Jeton d'authentification pour DELETE'\n"
        "    example: 'Bearer token'\n"
    ]

    assert errors == expected_errors, f"Les erreurs ne correspondent pas aux attentes. Reçues : {errors}"

def test_additional_headers(swagger_additional_headers, rules):
    validator = HeaderValidator(swagger_additional_headers, "", rules)
    errors = validator.validate_headers()
    
    expected_errors = [
        "Header 'Content-Type' est manquant dans GET /example. Il devrait être comme suit :\n"
        "  - name: 'Content-Type'\n"
        "    type: 'string'\n"
        "    required: True\n"
        "    description: 'Type de contenu pour GET'\n"
        "    example: 'application/json'\n"
    ]

    assert errors == expected_errors, f"Les erreurs ne correspondent pas aux attentes. Reçues : {errors}"
