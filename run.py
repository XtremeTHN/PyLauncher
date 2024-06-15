import os
import sys

from glob import glob
from src.modules.style import Logger
from src.modules.utils import check_call

SOURCE_DIR = os.getcwd()
RESOURCES_DIR = os.path.join(SOURCE_DIR, "src", "resources")
UI_DIR = os.path.join(SOURCE_DIR, "src", "ui")
BLP_DIR = os.path.join(UI_DIR, "blueprints")
BLP_FILES = glob(os.path.join(BLP_DIR, "*.blp"), recursive=True)

check_call("blueprint-compiler", "batch-compile", UI_DIR, BLP_DIR, *BLP_FILES, can_exit=True, buffer=sys.stdout)

check_call("glib-compile-resources", 
           "com.github.XtremeTHN.PyLauncherUI.gresource.xml", 
           wd=RESOURCES_DIR, can_exit=True, buffer=sys.stdout)

Logger.info("Notes:")
print("\t• If the libadwaita stylesheet not applying, it should be a problem related to callbacks")

check_call("python3", "test.py", wd="src", buffer=sys.stdout, can_exit=True)