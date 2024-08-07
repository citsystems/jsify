from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jsify",
    version="0.9.2",  # Update the version as necessary
    author="Zbigniew Rajewski",
    author_email="zbigniew.r@citsystems.pl",
    description="Jsify is a Python library designed to bridge the gap between Python's data structures and JSON-like "
                "objects, offering seamless integration and manipulation of data in a JavaScript-like manner."
                "With Jsify, you can effortlessly convert Python dictionaries, lists, and tuples into JSON-like "
                "objects that support attribute-style access, automatic handling of undefined properties, "
                "and easy serialization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="json javascript objects jsify dot attributes serialization",  # SEO keywords
    url="https://github.com/citsystems/jsify",  # Replace with the correct URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',  # Specify the required Python versions
    install_requires=[
        # List your project dependencies here
        # e.g., "requests >= 2.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
            "sphinx>=3.5.3",
            # Add other development dependencies
        ],
    },
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    project_urls={  # Optional: Additional URLs for the project
        "Documentation": "https://citsystems.github.io/jsify",
        "Source": "https://github.com/citsystems/jsify",
        "Tracker": "https://github.com/citsystems/jsify/issues",
    },
)
