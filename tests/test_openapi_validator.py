import pytest
from src.validators.openapi.openapi_validator import OpenAPIValidator

@pytest.fixture
def valid_swagger_v2():
    return {
        "swagger": "2.0",
        "info": {
            "version": "1.0.0",
            "title": "Valid API",
            "description": "A valid Swagger API"
        },
        "paths": {
            "/pet": {
                "get": {
                    "parameters": [
                        {
                            "name": "status",
                            "in": "query",
                            "type": "string",
                            "required": False
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation"
                        },
                        "400": {
                            "description": "Invalid status value"
                        }
                    }
                }
            }
        }
    }

@pytest.fixture
def invalid_swagger_v2():
    return {
        "swagger": "2.0",
        "info": {
            "version": "1.0.0",
            "title": "Invalid API",
            "description": "An invalid Swagger API"
        },
        "paths": {
            "/pet": {
                "get": {
                    "parameters": [
                        {
                            "name": "status",
                            "in": "query",
                            "type": "number",  # Incorrect type for this parameter
                            "required": False
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation"
                        },
                        "400": {
                            # Missing description
                        },
                        "default": {
                            "description": "default error"
                        }
                    }
                },
                "post": {
                    # Missing responses entirely
                }
            }
        }
    }

@pytest.fixture
def valid_openapi_v3():
    return {
        "openapi": "3.1.0",
        "info": {
            "version": "1.0.0",
            "title": "Valid API",
            "description": "A valid OpenAPI 3.0 API"
        },
        "paths": {
            "/pet": {
                "get": {
                    "parameters": [
                        {
                            "name": "status",
                            "in": "query",
                            "schema": {
                                "type": "string"
                            },
                            "required": False
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object"
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid status value",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "string"}
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
def invalid_openapi_v3():
    return {
        "openapi": "3.1.0",
        "info": {
            "version": "1.0.0",
            "title": "Invalid API",
            "description": "An invalid OpenAPI 3.0 API"
        },
        "paths": {
            "/pet": {
                "get": {
                    "parameters": [
                        {
                            "name": "status",
                            "in": "query",
                            "schema": {
                                "type": "number"  # Incorrect type for this parameter
                            },
                            "required": False
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object"
                                    }
                                }
                            }
                        },
                        "400": {
                            # Missing description
                        },
                        "500": {
                            "description": "Server error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "integer"}  # Incorrect type for error message
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    # Missing responses entirely
                }
            }
        }
    }

def test_valid_swagger_v2(valid_swagger_v2):
    swagger_text = "" 
    validator = OpenAPIValidator(valid_swagger_v2, swagger_text)
    result, message = validator.validate()
    assert result is True
    assert message == "Le swagger respecte la norme OpenAPI."

def test_invalid_swagger_v2(invalid_swagger_v2):
    swagger_text = "" 
    validator = OpenAPIValidator(invalid_swagger_v2, swagger_text)
    result, message = validator.validate()
    
    assert result is False
    assert "type" in message 
    assert "description" in message 
    assert "responses" in message 

def test_valid_openapi_v3(valid_openapi_v3):
    swagger_text = ""  
    validator = OpenAPIValidator(valid_openapi_v3, swagger_text)
    result, message = validator.validate()
    assert result is True
    assert message == "Le swagger respecte la norme OpenAPI."

def test_invalid_openapi_v3(invalid_openapi_v3):
    swagger_text = "" 
    validator = OpenAPIValidator(invalid_openapi_v3, swagger_text)
    result, message = validator.validate()
    
    # Vérifications supplémentaires
    assert result is False
    assert "type" in message  
    assert "description" in message  
    assert "responses" in message  
    assert "Erreur" in message 
