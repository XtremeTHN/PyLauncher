import os
import pathlib

from shutil import which
from datetime import datetime

MINECRAFT_DIR = pathlib.Path(pathlib.Path.home() / ".minecraft")
# PYLAUNCHER_CONFIG_FILE = pathlib.Path(MINECRAFT_DIR / "pylauncher" / "config.json")

LAUNCHER_CONFIG_FILE = pathlib.Path(MINECRAFT_DIR / "launcher_profiles.json")

# PYLAUNCHER_CONFIG_DIR = PYLAUNCHER_CONFIG_FILE.parent

DEFAULT_JVM_FLAGS = "-Xmx2G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M"
DEFAULT_LAUNCHER_CONFIG = {
    "profiles": {
        "default": {
            "name": "Default",
            "type": "custom",

            "created": datetime.now().isoformat(),
            "icon": "minecraft",

            "lastVersionId": "latest",
            "gameDir": str(MINECRAFT_DIR),

            "javaDir": which("java"),
            "javaArgs": DEFAULT_JVM_FLAGS,
            "resolution": {
                "width": 854,
                "height": 480
            },

            # Specific launcher options
            "disable-chat": False,
            "disable-multiplayer": False,

        }
    },
    "authenticationDatabase": {},

    "launcher":{
        # "closeAfterLaunch": True,
        "doAfterLaunch": "close",
        "show-snapshots": False,
        "show-old-versions": False,
        "show-alpha-versions": False
    },

    "selectedUser": "",

    "launcherVersion": {
        "name": "0.0.1",
        "format": 16,
        "profilesFormat": 1
    }
}