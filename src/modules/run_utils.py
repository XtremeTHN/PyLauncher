import xml.etree.ElementTree as ET
import sys
import os

from glob import glob
from .utils import check_call

SOURCE_DIR = os.getcwd()
RESOURCES_DIR = os.path.join(SOURCE_DIR, "src", "resources")
UI_DIR = os.path.join(SOURCE_DIR, "src", "ui", "xml")
UI_FILES = glob("ui/xml/*.ui", root_dir=os.path.join(SOURCE_DIR, "src"))
BLP_DIR = os.path.join(SOURCE_DIR, "src", "ui", "blueprints")
BLP_FILES = glob(os.path.join(BLP_DIR, "*.blp"), recursive=True)

class ResourcesFile:
    RES_TEMPLATE='<gresources><gresource prefix="/com/github/XtremeTHN/PyLauncherUI"></gresource></gresources>'

    def __init__(self):
        self.raw_resources_file_path = os.path.join(RESOURCES_DIR, "com.github.XtremeTHN.PyLauncherUI.gresource.xml")
        self.xml = ET.fromstring(self.RES_TEMPLATE)
        self.files = self.xml.find("gresource")
    
    def append(self, file: str):
        tag = ET.SubElement(self.files, "file")
        tag.text = f"../{file}"
        tag.attrib["alias"] = file.split("/")[-1]
    
    def compile(self):
        check_call("glib-compile-resources", 
           "com.github.XtremeTHN.PyLauncherUI.gresource.xml", 
            wd=RESOURCES_DIR, can_exit=True, buffer=sys.stdout)
    
    def save(self):
        ET.indent(self.xml)
        with open(self.raw_resources_file_path, "wb") as file:
            file.write(ET.tostring(self.xml))