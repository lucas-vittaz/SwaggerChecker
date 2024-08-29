import pytest
import json
from src.validators.projet.path_validator import PathValidator

@pytest.fixture
def reserved_paths():
    with open('config/projet_validation_rules.json', 'r') as f:
        config = json.load(f)
    return config["reserved_paths"]

@pytest.fixture
def swagger_dict_passant():
    return {
        "paths": {
            "/api/v1/public": {},
            "/api/v1/user": {},
            "/api/v1/pet": {}
        }
    }

@pytest.fixture
def swagger_dict_non_passant():
    return {
        "paths": {
            "/api/v1/admin/dashboard": {},
            "/api/v1/internal/stats": {},
            "/api/v1/public": {},
        }
    }

@pytest.fixture
def swagger_text():
    return """
    /api/v1/admin/dashboard:
    /api/v1/internal/stats:
    /api/v1/public:
    """

def test_validate_reserved_paths_passant(swagger_dict_passant, swagger_text, reserved_paths):
    validator = PathValidator(swagger_dict_passant, swagger_text, reserved_paths)
    errors = validator.validate_reserved_paths()
    assert len(errors) == 0, f"Des erreurs ont été trouvées dans un cas passant: {errors}"

def test_validate_reserved_paths_non_passant(swagger_dict_non_passant, swagger_text, reserved_paths):
    validator = PathValidator(swagger_dict_non_passant, swagger_text, reserved_paths)
    errors = validator.validate_reserved_paths()
    assert len(errors) == 2, f"Le nombre d'erreurs devrait être 2, mais est {len(errors)}. Erreurs: {errors}"
    assert "Le chemin '/api/v1/admin/dashboard' contient un mot réservé 'admin'" in errors[0]
    assert "Le chemin '/api/v1/internal/stats' contient un mot réservé 'internal'" in errors[1]
