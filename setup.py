# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="dasai",
    version="0.1.0",
    description="Group-Project for module Data-Science at TH Bingen.",
    long_description=readme,
    author="Miguel Mioskowski",
    author_email="miguel.mioskowski@th-bingen.de",
    url="https://github.com/migge898/DASC_STOCKMARKET_AI",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
)
