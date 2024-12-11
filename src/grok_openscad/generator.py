"""OpenSCAD code generator using Grok AI.

This module handles the generation of OpenSCAD code using the Grok AI API.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv


class GrokOpenSCAD:
    """Main class for generating OpenSCAD code using Grok AI."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GrokOpenSCAD generator.

        Args:
            api_key (Optional[str]): Grok API key. If not provided, will look for GROK_API_KEY in environment.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("GROK_API_KEY")
        print(f"self.api_key value: '{self.api_key}'")
        if not self.api_key:
            raise ValueError(
                "No Grok API key provided. Set GROK_API_KEY environment variable or pass key to constructor."
            )

        self.api_base = "https://api.x.ai/v1/chat/completions"
        self.last_generated_code = None
        self.system_prompt = """You are an OpenSCAD code generation assistant.
        You specialize in creating parametric 3D models that are optimized for 3D printing.
        Always provide complete, well-commented OpenSCAD code that follows best practices."""

    def generate(self, prompt: str, parameters: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate OpenSCAD code from a natural language prompt.

        Args:
            prompt (str): Natural language description of the desired 3D model
            parameters (Optional[Dict[str, Any]]): Additional parameters like temperature

        Returns:
            str: Generated OpenSCAD code
        """
        # Enhance prompt with OpenSCAD-specific context
        user_prompt = f"""
        Create OpenSCAD code for a 3D printable model with these requirements:
        {prompt}

        The code must be:
        - Parametric where appropriate
        - Well-commented
        - Following OpenSCAD best practices
        - Optimized for 3D printing

        Provide only the OpenSCAD code without any additional explanation.
        """

        try:
            response = self._call_grok_api(user_prompt, parameters)
            self.last_generated_code = self._extract_code(response)
            return self.last_generated_code
        except Exception as e:
            raise RuntimeError(f"Failed to generate OpenSCAD code: {str(e)}")

    def save_to_file(self, filename: str, code: Optional[str] = None) -> None:
        """
        Save generated OpenSCAD code to a file.

        Args:
            filename (str): Name of the file to save to
            code (Optional[str]): Code to save. If None, uses last generated code
        """
        code_to_save = code or self.last_generated_code
        if not code_to_save:
            raise ValueError("No code to save. Generate code first or provide code parameter.")

        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            f.write(code_to_save)

    def _call_grok_api(
        self, prompt: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API call to Grok."""
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

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

        response = requests.post(self.api_base, headers=headers, json=data)

        if response.status_code != 200:
            raise RuntimeError(f"API call failed: {response.text}")

        return response.json()

    def _extract_code(self, response: Dict[str, Any]) -> str:
        """Extract OpenSCAD code from API response and clean up code block markers."""
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
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Failed to extract code from response: {str(e)}")

    @staticmethod
    def validate_code(code: str) -> bool:
        """
        Validate OpenSCAD code syntax.

        Args:
            code (str): OpenSCAD code to validate

        Returns:
            bool: True if code is valid
        """
        # TODO: Implement OpenSCAD syntax validation
        # This could involve calling OpenSCAD CLI with --check-syntax
        return True
