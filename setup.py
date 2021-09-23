#!/usr/bin/env python

"""The setup script."""

from __future__ import annotations

from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

requirements: list[str] = []

requirements_dev = [
    "actions-toolkit>=0.0.5",
    "black>=21.5b0",
    "bump2version>=1.0.1",
    "codecov>=2.1.11",
    "coverage>=5.5",
    "dunamai>=1.5.5",
    "flake8>=3.9.1",
    "isort>=5.8.0",
    "mypy>=0.812",
    "pip-tools>=6.1.0",
    "pre-commit>=2.12.1",
    "pylint>=2.8.2",
    "pytest>=6.2.4",
    "pytest-cov>=2.11.1",
    "pytest-xdist>=2.2.1",
]

requirements_docs = [
    "Sphinx>=3.5.4",
    "sphinx-autoapi>=1.8.1",
]

requirements_dev += requirements_docs

setup(
    author="Sheypex",
    author_email="sheypex@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Higher level controlls for searching (a collection of) sklearn models for best parameters.",  # noqa: E501
    setup_requires=[
        "setuptools-git",
    ],
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
        "docs": requirements_docs,
    },
    license="BSD-3-Clause",
    long_description=readme + "\n\n" + history,
    name="sklearn_tournament",
    packages=find_packages(include=["sklearn_tournament", "sklearn_tournament.*"]),
    include_package_data=True,
    test_suite="tests",
    url="https://github.com/sheypex/sklearn-tournament",
    version="0.1.0",
    zip_safe=False,
)
