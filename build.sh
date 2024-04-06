#!/bin/bash

python3 -m nuitka --follow-imports src/main.py -o pylauncher

sudo cp pylauncher /usr/bin/pylauncher