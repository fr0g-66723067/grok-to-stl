"""
Grok-OpenSCAD Generator Module
This module provides the main interface for generating OpenSCAD code using Grok AI.
"""

import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional, Dict, Any

class GrokOpenSCAD:
    """Main class for generating OpenSCAD code using Grok AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GrokOpenSCAD generator.
        
        Args:
            api_key (Optional[str]): Grok API key. If not provided, will look for GROK_API_KEY in environment.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('GROK_API_KEY')
        if not self.api_key:
            raise ValueError("No Grok API key provided. Set GROK_API_KEY environment variable or pass key to constructor.")
        
        self.api_base = "https://api.grok.x.ai/v1"
        self.last_generated_code = None
    
    def generate(self, prompt: str, parameters: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate OpenSCAD code from a natural language prompt.
        
        Args:
            prompt (str): Natural language description of the desired 3D model
            parameters (Optional[Dict[str, Any]]): Additional parameters for generation
            
        Returns:
            str: Generated OpenSCAD code
        """
        # Enhance prompt with OpenSCAD-specific context
        enhanced_prompt = f"""
        Generate OpenSCAD code for a 3D printable model with the following requirements:
        {prompt}
        
        Requirements:
        - Code should be parametric where appropriate
        - Include helpful comments
        - Follow OpenSCAD best practices
        - Ensure the model is 3D printable
        """
        
        try:
            response = self._call_grok_api(enhanced_prompt, parameters)
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
        
        with open(path, 'w') as f:
            f.write(code_to_save)
    
    def _call_grok_api(self, prompt: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make API call to Grok."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "parameters": parameters or {}
        }
        
        response = requests.post(
            f"{self.api_base}/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"API call failed: {response.text}")
        
        return response.json()
    
    def _extract_code(self, response: Dict[str, Any]) -> str:
        """Extract OpenSCAD code from API response."""
        # Implementation depends on actual Grok API response format
        # This is a placeholder implementation
        try:
            return response.get("choices", [{}])[0].get("text", "").strip()
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