import pytest
from src.validators.projet.responses.response_validator import ResponseValidator

@pytest.fixture
def swagger_responses_with_refs():
    return {
        "components": {
            "schemas": {
                "ErrorResponse": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                        "error_description": {"type": "string"}
                    }
                }
            }
        },
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
                                        "$ref": "#/components/schemas/ErrorResponse"
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
def swagger_responses_with_empty_objects():
    return {
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

def test_valid_responses_with_refs(swagger_responses_with_refs, rules):
    validator = ResponseValidator(swagger_responses_with_refs, "", rules)
    errors = validator.validate_responses()
    assert not errors, f"Aucune erreur ne devrait être trouvée pour des réponses valides avec références, mais les erreurs suivantes ont été trouvées : {errors}"

def test_valid_responses_with_empty_objects(swagger_responses_with_empty_objects, rules):
    validator = ResponseValidator(swagger_responses_with_empty_objects, "", rules)
    errors = validator.validate_responses()
    assert not errors, f"Aucune erreur ne devrait être trouvée pour des réponses valides avec des objets vides ou des tableaux d'objets, mais les erreurs suivantes ont été trouvées : {errors}"

def test_invalid_ref_resolution(swagger_responses_with_refs, rules):
    swagger_responses_with_refs["paths"]["/example"]["get"]["responses"]["400"]["content"]["application/json"]["schema"]["$ref"] = "#/components/schemas/NonExistentSchema"
    validator = ResponseValidator(swagger_responses_with_refs, "", rules)
    errors = validator.validate_responses()
    assert errors, "Une erreur devrait être trouvée pour une référence non résolue."

def test_missing_response(swagger_responses_with_refs, rules):
    del swagger_responses_with_refs["paths"]["/example"]["get"]["responses"]["200"]
    validator = ResponseValidator(swagger_responses_with_refs, "", rules)
    errors = validator.validate_responses()
    assert errors, "Une erreur devrait être trouvée pour une réponse manquante."
