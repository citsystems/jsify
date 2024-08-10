import os
from types import SimpleNamespace
from setuptools import find_packages

module_dir = os.path.dirname(__file__)


class Setup:
    def __init__(self):
        # Read the contents of the README file
        with open(module_dir + "/README.md", "r", encoding="utf-8") as fh:
            long_description = fh.read()
        self.name = "jsify"
        self.version = "0.9.6"  # Update the version as necessary
        self.author = "Zbigniew Rajewski"
        self.author_email = "zbigniew.r@citsystems.pl"
        self.description = \
            "Jsify is a Python library designed to bridge the gap between Python's data structures and JSON-like " \
            "objects, offering seamless integration and manipulation of data in a JavaScript-like manner." \
            "With Jsify, you can effortlessly convert Python dictionaries, lists, and tuples into JSON-like " \
            "objects that support attribute-style access (dot notation), automatic handling of undefined " \
            "properties, and easy serialization."
        self.long_description = long_description
        self.long_description_content_type = "text/markdown"
        self.keywords = "json javascript objects jsify dot notation attributes serialization"  # SEO keywords
        self.url = "https://github.com/citsystems/jsify"  # Replace with the correct URL
        self.packages = find_packages()
        self.classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
        self.python_requires = '>=3.0'  # Specify the required Python versions
        self.install_requires = [
            # List your project dependencies here
            # e.g., "requests >= 2.20.0",
        ]
        self.extras_require = {
            "dev": [
                "pytest>=3.7",
                "sphinx>=3.5.3",
                # Add other development dependencies
            ],
        }
        self.include_package_data = True  # Include non-Python files specified in MANIFEST.in
        self.project_urls = {  # Optional: Additional URLs for the project
            "Documentation": "https://citsystems.github.io/jsify",
            "Source": "https://github.com/citsystems/jsify",
            "Tracker": "https://github.com/citsystems/jsify/issues",
        }

setup = Setup()
