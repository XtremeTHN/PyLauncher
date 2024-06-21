import uuid
import pathlib

from shutil import which
from datetime import datetime

from minecraft_launcher_lib.utils import get_java_executable
from pylauncher.backend.types import LauncherStandardConfig, PyLauncherConfig

MINECRAFT_DIR = pathlib.Path(pathlib.Path.home() / ".minecraft")
PYLAUNCHER_CONFIG_FILE = pathlib.Path(MINECRAFT_DIR / "pylauncher" / "config.json")
PYLAUNCHER_CONFIG_DIR = PYLAUNCHER_CONFIG_FILE.parent
PYLAUNCHER_DEFAULT_CONFIG: PyLauncherConfig = {
    "doAfterLaunch": "close",
    "show_snapshots": False,
    "show_beta_versions": False,
    "show_alpha_versions": False
}

LAUNCHER_PROFILES_CONFIG_FILE = pathlib.Path(MINECRAFT_DIR / "launcher_profiles.json")

DEFAULT_JVM_FLAGS = "-Xmx2G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M"
DEFAULT_LAUNCHER_PROFILES_CONFIG: LauncherStandardConfig = {
    "profiles": {
        "default": {
            "name": "Default",
            "type": "custom",

            "created": datetime.now().isoformat(),

            "lastVersionId": "latest",
            "gameDir": str(MINECRAFT_DIR),

            "javaDir": which("java"),
            "javaArgs": "",
            "resolution": {
                "width": 854,
                "height": 480
            },
        }
    },
    "authenticationDatabase": {},
    "clientToken": str(uuid.uuid4()),

    "selectedProfile": "default",

    "selectedUser": "",

    "launcherVersion": {
        "name": "0.0.1",
        "format": 16,
        "profilesFormat": 1
    }
}

DEFAULT_MINECRAFT_WINDOW_WIDTH=854
DEFAULT_MINECRAFT_WINDOW_HEIGHT=480

JAVA_PATH=get_java_executable()

DEFAULT_PROFILE_PAGE_CHILD_ICON = "image-missing-symbolic"
