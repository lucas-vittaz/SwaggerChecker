import pytest
from src.utils.swagger_loader import load_swagger

@pytest.fixture
def create_temp_json_file(tmp_path):
    def _create_temp_json_file(content):
        file_path = tmp_path / "swagger.json"
        file_path.write_text(content)
        return str(file_path) 
    return _create_temp_json_file

@pytest.fixture
def create_temp_yaml_file(tmp_path):
    def _create_temp_yaml_file(content):
        file_path = tmp_path / "swagger.yaml"
        file_path.write_text(content)
        return str(file_path)  
    return _create_temp_yaml_file

def test_load_valid_json(create_temp_json_file):
    valid_json_swagger = '{"swagger": "2.0", "info": {"title": "Sample API", "version": "1.0.0"}}'
    file_path = create_temp_json_file(valid_json_swagger)
    loaded_swagger = load_swagger(file_path)
    assert loaded_swagger["swagger"] == "2.0"

def test_load_valid_yaml(create_temp_yaml_file):
    valid_yaml_swagger = "swagger: '2.0'\ninfo:\n  title: Sample API\n  version: '1.0.0'"
    file_path = create_temp_yaml_file(valid_yaml_swagger)
    loaded_swagger = load_swagger(file_path)
    assert loaded_swagger["swagger"] == "2.0"

def test_unsupported_file_extension(tmp_path):
    file_path = tmp_path / "swagger.txt"
    file_path.write_text("Unsupported content")
    with pytest.raises(ValueError, match="Unsupported file format"):
        load_swagger(str(file_path))
