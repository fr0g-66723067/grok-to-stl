# AI-Generated 3D Models with Grok and OpenSCAD

This project demonstrates how to use generative AI (specifically Grok) to create parametric 3D models using OpenSCAD for 3D printing. The project aims to bridge the gap between natural language descriptions and 3D printable models.

## 🚀 Features

- Natural language to OpenSCAD code conversion using Grok
- Parametric 3D model generation
- Ready-to-print STL file output
- Example models and use cases
- Comprehensive documentation
- Command-line interface for quick generation

## 📋 Prerequisites

- OpenSCAD (latest version)
- Access to Grok AI
- Python 3.8+
- Basic understanding of 3D printing concepts

## 🛠️ Installation

1. Clone this repository: 
```bash
git clone https://github.com/fr0g-66723067/grok-to-stl.git
cd grok-to-stl
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Documentation

See the [docs](./docs) directory for comprehensive documentation including:
- Getting Started Guide
- API Reference
- Example Projects
- Best Practices
- Troubleshooting Guide

## 🎯 Quick Start

### Using Python API

```python
from grok_openscad import GrokOpenSCAD

# Initialize the generator
generator = GrokOpenSCAD()

# Generate a simple model
scad_code = generator.generate("Create a cylindrical vase with a height of 100mm and diameter of 50mm")

# Save to file and convert to STL
generator.save_to_file("vase.scad")
```

### Using Command Line

Generate an example model:
```bash
grok-to-stl --example cube --output cube.scad
```

Generate a custom model:
```bash
grok-to-stl --prompt "Create a hexagonal pencil holder with height 100mm" --output holder.scad
```

Convert to STL:
```bash
openscad -o model.stl output.scad
```

### CLI Options

- `--prompt TEXT`: Natural language description of the model to generate
- `--example [cube|vase|box]`: Generate a pre-defined example model
- `--output FILE`: Output file name (default: output.scad)
- `--api-key KEY`: Grok API key (can also be set via GROK_API_KEY environment variable)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenSCAD community
- Grok AI team
- All contributors and users of this project