# Getting Started with Grok-to-STL

This guide will help you get started with using Grok AI to generate 3D printable models through OpenSCAD.

## Prerequisites

Before you begin, ensure you have:

1. Python 3.8 or higher installed
2. OpenSCAD installed ([Download here](https://openscad.org/downloads.html))
3. A Grok API key ([Get access here](https://grok.x.ai))
4. Git installed

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fr0g-66723067/grok-to-stl.git
cd grok-to-stl
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Grok API key:
Create a `.env` file in the project root and add:
```
GROK_API_KEY=your_api_key_here
```

## Basic Usage

### 1. Simple Model Generation

```python
from grok_openscad import GrokOpenSCAD

# Initialize the generator
generator = GrokOpenSCAD()

# Generate a simple cube
scad_code = generator.generate("Create a cube with 30mm sides")

# Save to file
generator.save_to_file("cube.scad")
```

### 2. Parametric Models

```python
# Generate a parametric box
prompt = """
Create a parametric box with:
- Variable height (default 100mm)
- Variable width (default 80mm)
- Variable length (default 120mm)
- Rounded corners (radius 5mm)
- Wall thickness 2mm
"""

scad_code = generator.generate(prompt)
generator.save_to_file("parametric_box.scad")
```

### 3. Converting to STL

After generating your SCAD file, you can convert it to STL using either:

1. OpenSCAD GUI: Open the file and export as STL
2. Command line:
```bash
openscad -o output.stl input.scad
```

## Best Practices

1. **Be Specific in Prompts**
   - Include precise measurements
   - Specify any constraints
   - Mention important features

2. **Validate Models**
   - Always preview in OpenSCAD before printing
   - Check for manifold geometry
   - Verify wall thicknesses

3. **Organize Your Files**
   - Keep SCAD files in the `examples` directory
   - Document parameter usage
   - Add comments to complex designs

## Next Steps

- Check out the [examples](../examples/) directory for more complex models
- Read the [API Reference](./api_reference.md) for detailed function documentation
- Learn about [parameterization](./examples/parameters.md)
- Explore [advanced features](./examples/complex_models.md)

## Troubleshooting

If you encounter issues:

1. Verify your Grok API key is correctly set
2. Check OpenSCAD installation and version
3. Ensure all dependencies are installed
4. See [troubleshooting guide](./troubleshooting.md) for common issues

## Getting Help

- Open an issue on GitHub
- Check existing issues for solutions
- Read the [FAQ](./faq.md)
- Join our community discussions 