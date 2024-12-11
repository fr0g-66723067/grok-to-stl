# Project Structure

This document outlines the organization of the project files and directories.

```
project-root/
├── docs/                      # Documentation files
│   ├── getting_started.md     # Quick start guide
│   ├── api_reference.md       # API documentation
│   ├── examples/              # Example documentation
│   │   ├── basic_shapes.md    # Basic shape examples
│   │   ├── complex_models.md  # Complex model examples
│   │   └── parameters.md      # Parameter usage guide
│   ├── best_practices.md      # Best practices guide
│   └── troubleshooting.md     # Common issues and solutions
│
├── src/                       # Source code
│   ├── grok_openscad/        # Main package
│   │   ├── __init__.py
│   │   ├── generator.py      # Core generation logic
│   │   ├── converter.py      # SCAD conversion utilities
│   │   └── validator.py      # Code validation
│   └── utils/                # Utility functions
│       ├── __init__.py
│       └── helpers.py
│
├── examples/                  # Example SCAD files
│   ├── basic/
│   │   ├── cube.scad
│   │   └── sphere.scad
│   └── advanced/
│       ├── parametric_box.scad
│       └── vase.scad
│
├── templates/                 # SCAD templates
│   ├── basic_object.scad
│   └── parametric_object.scad
│
├── tests/                    # Test files
│   ├── __init__.py
│   ├── test_generator.py
│   └── test_converter.py
│
├── .gitignore               # Git ignore file
├── LICENSE                  # MIT license
├── README.md               # Project overview
├── CONTRIBUTING.md         # Contribution guidelines
├── requirements.txt        # Python dependencies
└── setup.py               # Package setup file
```

## Directory Details

### `/docs`
Contains all project documentation, including guides, API reference, and examples.

### `/src`
Core source code for the project, including the main package and utilities.

### `/examples`
Ready-to-use example files demonstrating various use cases.

### `/templates`
Base templates for generating different types of 3D models.

### `/tests`
Test suite ensuring code quality and functionality.

## Key Files

- `requirements.txt`: Lists all Python package dependencies
- `setup.py`: Package installation and distribution settings
- `CONTRIBUTING.md`: Guidelines for contributing to the project
- `LICENSE`: MIT license terms
- `README.md`: Project overview and quick start guide
