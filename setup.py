"""
Setup configuration for grok-openscad package.

This module contains the package configuration and dependencies required
for installing and distributing the grok-openscad package.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grok-to-stl",
    version="0.1.0",
    author="fr0g-66723067",
    author_email="",  # Add your email if you want
    description="Generate 3D printable models using Grok AI and OpenSCAD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fr0g-66723067/grok-to-stl",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: CAD",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.3.0",
            "flake8>=6.0.0",
        ],
        "build": [
            "setuptools>=68.0.0",
            "wheel>=0.40.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "grok-to-stl=grok_openscad.cli:main",
        ],
    },
)
