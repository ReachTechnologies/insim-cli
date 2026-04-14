#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages
import os

here = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(here, "cli_anything", "insim", "README.md")
long_description = open(readme_path, "r", encoding="utf-8").read() if os.path.exists(readme_path) else ""

setup(
    name="insim-cli",
    version="1.0.1",
    author="Reach Technologies SAS",
    author_email="dev@reach-technologies.com",
    description="inSIM CLI — Control your SMS, contacts and campaigns from the command line. Built for AI agents and humans alike.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ReachTechnologies/insim-cli",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Telephony",
        "Topic :: Office/Business",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0.0",
        "requests>=2.28.0",
        "prompt-toolkit>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "insim=cli_anything.insim.insim_cli:main",
        ],
    },
    package_data={
        "cli_anything.insim": ["skills/*.md", "README.md"],
    },
    include_package_data=True,
    zip_safe=False,
)
