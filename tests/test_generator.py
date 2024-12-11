"""
Tests for the OpenSCAD code generator.
"""

import os
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
    # Mock load_dotenv to do nothing
    monkeypatch.setattr("dotenv.load_dotenv", lambda: None)

    # Mock os.getenv to always return None for GROK_API_KEY
    def mock_getenv(key, default=None):
        if key == "GROK_API_KEY":
            return None
        return os.getenv(key, default)

    monkeypatch.setattr("os.getenv", mock_getenv)

    print(f"Environment GROK_API_KEY: '{os.getenv('GROK_API_KEY')}'")
    with pytest.raises(ValueError):
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

    with pytest.raises(RuntimeError):
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
    # Note: This is a placeholder test since validate_code
    # currently always returns True
    assert GrokOpenSCAD.validate_code("cube([10, 10, 10]);") is True


if __name__ == "__main__":
    pytest.main([__file__])
