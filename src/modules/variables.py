import uuid
import pathlib

from shutil import which
from datetime import datetime

from modules.types import LauncherStandardConfigType, PyLauncherConfigType

MINECRAFT_DIR = pathlib.Path(pathlib.Path.home() / ".minecraft")
PYLAUNCHER_CONFIG_FILE = pathlib.Path(MINECRAFT_DIR / "pylauncher" / "config.json")
PYLAUNCHER_CONFIG_DIR = PYLAUNCHER_CONFIG_FILE.parent
PYLAUNCHER_DEFAULT_CONFIG: PyLauncherConfigType = {
    "doAfterLaunch": "close",
    "show_snapshots": False,
    "show_beta_versions": False,
    "show_alpha_versions": False
}

LAUNCHER_PROFILES_CONFIG_FILE = pathlib.Path(MINECRAFT_DIR / "launcher_profiles.json")

DEFAULT_JVM_FLAGS = "-Xmx2G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M"
DEFAULT_LAUNCHER_PROFILES_CONFIG: LauncherStandardConfigType = {
    "profiles": {
        "default": {
            "name": "Default",
            "type": "custom",

            "created": datetime.now().isoformat(),
            "icon": "minecraft",

            "lastVersionId": "latest",
            "gameDir": str(MINECRAFT_DIR),

            "javaDir": which("java"),
            "javaArgs": None,
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