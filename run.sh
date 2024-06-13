#!/bin/bash

SOURCE_DIR=$(pwd)

cd src/ui
blueprint-compiler compile main.blp --output main.ui
glib-compile-resources com.github.XtremeTHN.PyLauncherUI.gresource.xml
cd $SOURCE_DIR

python3 src/test.py