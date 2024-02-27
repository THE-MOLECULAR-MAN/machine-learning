#!/bin/bash
# Tim H 2024

# jupyter nbconvert --to python cbb-dataprep.ipynb
# pylint cbb-dataprep.py

jupyter nbconvert cbb-dataprep.ipynb --stdout --to python --PythonExporter.exclude_markdown=True | flake8 - --ignore=W391
