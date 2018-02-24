#!/bin/bash

cd `dirname $0`
cd ../docs
make clean
make html
cd ./_build/html
python -m http.server
