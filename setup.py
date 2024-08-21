from setuptools import setup, find_packages

setup(
    name="swagger-validator",
    version="0.1.0",
    description="A Python project to validate Swagger (OpenAPI) specifications and ensure they meet project-specific rules.",
    author="Votre Nom",
    author_email="votre.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openapi-spec-validator",
        "PyYAML",
        "tkinter"  # Note: tkinter is part of the standard library, no need to install separately
    ],
    entry_points={
        "console_scripts": [
            "swagger-validator=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
