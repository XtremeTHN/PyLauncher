import pathlib

# Remove when the project is finished
_TEST_DATA_DIR = "/home/axel/Documents/Projects/LinuxProjects/PyLauncherUi"

# Change when the project is finished
DATA_DIR = pathlib.Path(_TEST_DATA_DIR) / "src"

RESOURCES_FILE = DATA_DIR / "resources" / "com.github.XtremeTHN.PyLauncherUI.gresource"

# Remove when the project is finished
DATA_DIR.mkdir(exist_ok=True)