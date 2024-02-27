#!/bin/bash
# Tim H 2024

# jupyter nbconvert --to python cbb-dataprep.ipynb

clear

for iter_filename in *.ipynb; do
    black "$iter_filename"
    # intentionally storing it in a file so I can see context, 
    # not just a line number
    TMP_FILENAME="${iter_filename}.py.tmp"
    jupyter nbconvert "$iter_filename" --stdout --to python --PythonExporter.exclude_markdown=True > "${TMP_FILENAME}"
    # flake8 --ignore=W391 "${iter_filename}.py.tmp"
    echo "Checking Lint for $TMP_FILENAME..."
    pylint --rcfile=../.pylintrc "${TMP_FILENAME}"

done