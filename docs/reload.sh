#!/bin/bash

cd `dirname $0`
cd ../
sphinx-apidoc -F -o docs/ src/
cd ./docs
make clean
make html
cd ./_build/html
python -m http.server
