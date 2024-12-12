"""Module for generating OpenSCAD code using Grok AI."""

import os
from typing import Any, Dict, Optional

import pytest
import requests
from dotenv import load_dotenv


class GrokOpenSCAD:
    """Main class for generating OpenSCAD code using Grok AI."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the GrokOpenSCAD generator.

        Args:
            api_key: Optional Grok API key. If not provided, will look for
                    GROK_API_KEY in environment.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("GROK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No Grok API key provided. Set GROK_API_KEY environment variable "
                "or pass key to constructor."
            )

        self.api_base = "https://api.x.ai/v1/chat/completions"
        self.last_generated_code = None
        self.system_prompt = (
            "You are an OpenSCAD code generation assistant. "
            "You specialize in creating parametric 3D models that are optimized "
            "for 3D printing. Always provide complete, well-commented OpenSCAD code."
        )

    def generate(self, prompt: str, parameters: Optional[Dict[str, Any]] = None) -> str:
        """Generate OpenSCAD code from a natural language prompt.

        Args:
            prompt: Natural language description of the desired 3D model
            parameters: Optional parameters like temperature

        Returns:
            Generated OpenSCAD code
        """
        # Enhance prompt with OpenSCAD-specific context
        user_prompt = (
            "Create OpenSCAD code for a 3D printable model with these requirements:\n"
            f"{prompt}\n\n"
            "The code must be:\n"
            "- Parametric where appropriate\n"
            "- Well-commented\n"
            "- Following OpenSCAD best practices\n"
            "- Optimized for 3D printing\n\n"
            "Provide only the OpenSCAD code without any additional explanation."
        )

        try:
            response = self._call_grok_api(user_prompt, parameters)
            self.last_generated_code = self._extract_code(response)
            return self.last_generated_code
        except Exception as e:
            raise RuntimeError(f"Failed to generate OpenSCAD code: {str(e)}")

    def save_to_file(self, filename: str) -> None:
        """Save generated OpenSCAD code to a file.

        Args:
            filename: Name of the file to save to
        """
        if not self.last_generated_code:
            raise ValueError("No code to save. Generate code first.")

        with open(filename, "w") as f:
            f.write(self.last_generated_code)

    def _call_grok_api(
        self, prompt: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API call to Grok.

        Args:
            prompt: The prompt to send to the API
            parameters: Optional API parameters

        Returns:
            API response data
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        data = {
            "messages": messages,
            "model": "grok-beta",
            "stream": False,
            "temperature": parameters.get("temperature", 0.7) if parameters else 0.7,
        }

        response = requests.post(
            self.api_base,
            headers=headers,
            json=data,
        )

        if response.status_code != 200:
            raise RuntimeError(f"API call failed: {response.text}")

        return response.json()

    def _extract_code(self, response: Dict[str, Any]) -> str:
        """Extract OpenSCAD code from API response and clean up code block markers.

        Args:
            response: API response data

        Returns:
            Extracted OpenSCAD code with markers removed
        """
        try:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

            # Remove code block markers if present
            if content.startswith("```openscad"):
                content = content[len("```openscad") :].strip()
            elif content.startswith("```"):
                content = content[3:].strip()

            if content.endswith("```"):
                content = content[:-3].strip()

            return content
        except (KeyError, IndexError) as e:  # pragma: no cover
            raise RuntimeError(
                f"Failed to extract code from response: {str(e)}"
            )  # pragma: no cover

    @staticmethod
    def validate_code(code: str) -> bool:
        """Validate OpenSCAD code syntax.

        Args:
            code: OpenSCAD code to validate

        Returns:
            True if code is valid, False otherwise
        """
        if not code:  # Handles None and empty string cases
            return False
        # TODO: Implement OpenSCAD syntax validation
        return True


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__])  # pragma: no cover
