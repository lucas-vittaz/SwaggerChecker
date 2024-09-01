import pytest
from src.validators.projet.responses.response_validator import ResponseValidator

@pytest.fixture
def swagger_responses():
    return {
        "paths": {
            "/example": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Requête réussie",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Requête incorrecte",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "error": {"type": "string"},
                                                "error_description": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

@pytest.fixture
def rules():
    return {
        "GET": {
            "responses": [
                {
                    "response_code": 200,
                    "format": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"}
                        }
                    }
                },
                {
                    "response_code": 400,
                    "format": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string"},
                                "error_description": {"type": "string"}
                            }
                        }
                    }
                }
            ]
        }
    }

def test_valid_responses(swagger_responses, rules):
    validator = ResponseValidator(swagger_responses, "", rules)
    errors = validator.validate_responses()
    assert not errors, f"Aucune erreur ne devrait être trouvée pour des réponses valides, mais les erreurs suivantes ont été trouvées : {errors}"

def test_invalid_response_type(swagger_responses, rules):
    swagger_responses["paths"]["/example"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["type"] = "array"
    validator = ResponseValidator(swagger_responses, "", rules)
    errors = validator.validate_responses()
    assert errors, "Une erreur devrait être trouvée pour un type de réponse incorrect."

def test_missing_response(swagger_responses, rules):
    del swagger_responses["paths"]["/example"]["get"]["responses"]["200"]
    validator = ResponseValidator(swagger_responses, "", rules)
    errors = validator.validate_responses()
    assert errors, "Une erreur devrait être trouvée pour une réponse manquante."

def test_valid_responses_with_empty_objects():
    swagger_responses_with_empty_objects = {
        "paths": {
            "/example": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Requête réussie",
                            "content": {
                                "application/json": {
                                    "schema": {}
                                }
                            }
                        },
                        "400": {
                            "description": "Requête incorrecte",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "error": {"type": "string"},
                                                "error_description": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    rules = {
        "GET": {
            "responses": [
                {
                    "response_code": 200,
                    "format": {}
                },
                {
                    "response_code": 400,
                    "format": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string"},
                                "error_description": {"type": "string"}
                            }
                        }
                    }
                }
            ]
        }
    }
    validator = ResponseValidator(swagger_responses_with_empty_objects, "", rules)
    errors = validator.validate_responses()
    assert not errors, f"Aucune erreur ne devrait être trouvée pour des réponses valides avec des objets vides ou des tableaux d'objets, mais les erreurs suivantes ont été trouvées : {errors}"

def test_invalid_response_format():
    swagger_responses_invalid = {
        "paths": {
            "/example": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Requête réussie",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "integer"}  # Type incorrect
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    rules = {
        "GET": {
            "responses": [
                {
                    "response_code": 200,
                    "format": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"}
                        }
                    }
                }
            ]
        }
    }
    validator = ResponseValidator(swagger_responses_invalid, "", rules)
    errors = validator.validate_responses()
    assert errors, "Une erreur devrait être trouvée pour un format de réponse incorrect."
