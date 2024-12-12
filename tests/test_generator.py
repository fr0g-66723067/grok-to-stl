"""Tests for the OpenSCAD code generator."""

from unittest.mock import MagicMock, patch

import pytest

from grok_openscad.generator import GrokOpenSCAD


@pytest.fixture
def mock_env_api_key(monkeypatch):
    """Fixture to mock environment variable."""
    monkeypatch.setenv("GROK_API_KEY", "test_key")


@pytest.fixture
def generator(mock_env_api_key):
    """Fixture to create a GrokOpenSCAD instance."""
    return GrokOpenSCAD()


def test_init_with_env_key(mock_env_api_key):
    """Test initialization with environment variable."""
    gen = GrokOpenSCAD()
    assert gen.api_key == "test_key"


def test_init_with_provided_key():
    """Test initialization with provided API key."""
    gen = GrokOpenSCAD(api_key="provided_key")
    assert gen.api_key == "provided_key"


def test_init_without_key(monkeypatch):
    """Test initialization without any API key."""
    monkeypatch.setattr("dotenv.load_dotenv", lambda: None)
    monkeypatch.setattr("os.getenv", lambda key, default=None: None)

    with pytest.raises(ValueError, match="No Grok API key provided"):
        GrokOpenSCAD()


@patch("requests.post")
def test_generate_success(mock_post, generator):
    """Test successful code generation."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "```openscad\ncube([10, 10, 10]);\n```"}}]
    }
    mock_post.return_value = mock_response

    code = generator.generate("Create a simple cube")
    assert code == "cube([10, 10, 10]);"
    assert generator.last_generated_code == code


@patch("requests.post")
def test_generate_api_error(mock_post, generator):
    """Test API error handling."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "API Error"
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="Failed to generate OpenSCAD code"):
        generator.generate("Create a cube")


def test_save_to_file(generator, tmp_path):
    """Test saving code to file."""
    test_code = "cube([10, 10, 10]);"
    generator.last_generated_code = test_code

    file_path = tmp_path / "test.scad"
    generator.save_to_file(str(file_path))

    assert file_path.read_text() == test_code


def test_save_to_file_no_code(generator):
    """Test saving when no code is available."""
    with pytest.raises(ValueError):
        generator.save_to_file("test.scad")


def test_validate_code():
    """Test code validation."""
    assert GrokOpenSCAD.validate_code("cube([10, 10, 10]);") is True


def test_validate_code_invalid():
    """Test code validation with invalid code."""
    assert GrokOpenSCAD.validate_code("") is False
    assert GrokOpenSCAD.validate_code(None) is False


@patch("requests.post")
def test_extract_code_with_generic_markers(mock_post, generator):
    """Test code extraction with generic code block markers."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "```\ncube([10, 10, 10]);\n```"}}]
    }
    mock_post.return_value = mock_response

    code = generator.generate("Create a simple cube")
    assert code == "cube([10, 10, 10]);"


@patch("requests.post")
def test_extract_code_without_markers(mock_post, generator):
    """Test code extraction without any code block markers."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"choices": [{"message": {"content": "cube([10, 10, 10]);"}}]}
    mock_post.return_value = mock_response

    code = generator.generate("Create a simple cube")
    assert code == "cube([10, 10, 10]);"


@patch("requests.post")
def test_extract_code_malformed_response(mock_post, generator):
    """Test code extraction with malformed API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}

    with pytest.raises(RuntimeError, match="Failed to generate OpenSCAD code"):
        generator.generate("Create a cube")


@patch("requests.post")
def test_extract_code_missing_content(mock_post, generator):
    """Test code extraction with missing content in response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"choices": [{"message": {"content": None}}]}

    with pytest.raises(RuntimeError, match="Failed to generate OpenSCAD code"):
        generator.generate("Create a cube")


@patch("requests.post")
def test_extract_code_key_error(mock_post, generator):
    """Test code extraction with KeyError in response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"invalid_key": []}

    with pytest.raises(RuntimeError, match="Failed to generate OpenSCAD code"):
        generator.generate("Create a cube")


@patch("requests.post")
def test_generate_with_parameters(mock_post, generator):
    """Test code generation with custom parameters."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"choices": [{"message": {"content": "cube([10, 10, 10]);"}}]}
    mock_post.return_value = mock_response

    parameters = {"temperature": 0.5}
    code = generator.generate("Create a simple cube", parameters=parameters)
    assert code == "cube([10, 10, 10]);"

    # Verify the API was called with the correct parameters
    called_data = mock_post.call_args[1]["json"]
    assert called_data["temperature"] == 0.5


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__])  # pragma: no cover
