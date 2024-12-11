"""
Command-line interface for Grok-to-STL.
"""

import argparse
import os
import sys
from pathlib import Path
from .generator import GrokOpenSCAD

EXAMPLE_PROMPTS = {
    'cube': "Create a parametric cube with 30mm sides and rounded corners of radius 2mm",
    'vase': "Create a cylindrical vase with height 100mm, diameter 50mm, and wall thickness 2mm that can hold water",
    'box': """Create a parametric box with:
    - Variable height (default 100mm)
    - Variable width (default 80mm)
    - Variable length (default 120mm)
    - Rounded corners (radius 5mm)
    - Wall thickness 2mm""",
}

def main():
    parser = argparse.ArgumentParser(
        description="Generate 3D printable models using Grok AI and OpenSCAD"
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        help='Natural language description of the 3D model to generate'
    )
    
    parser.add_argument(
        '--example',
        choices=list(EXAMPLE_PROMPTS.keys()),
        help='Generate an example model (cube, vase, or box)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='output.scad',
        help='Output file name (default: output.scad)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='Grok API key (can also be set via GROK_API_KEY environment variable)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.prompt and not args.example:
        parser.error("Either --prompt or --example must be specified")
    
    if args.prompt and args.example:
        parser.error("Cannot specify both --prompt and --example")
    
    try:
        # Initialize generator
        generator = GrokOpenSCAD(api_key=args.api_key)
        
        # Get the prompt
        prompt = args.prompt if args.prompt else EXAMPLE_PROMPTS[args.example]
        
        print(f"Generating OpenSCAD code for: {prompt}")
        
        # Generate the code
        code = generator.generate(prompt)
        
        # Save to file
        output_path = Path(args.output)
        generator.save_to_file(str(output_path))
        
        print(f"\nSuccess! OpenSCAD code has been saved to: {output_path}")
        print("\nYou can now:")
        print(f"1. Open the file in OpenSCAD: openscad {output_path}")
        print(f"2. Convert to STL: openscad -o {output_path.stem}.stl {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 