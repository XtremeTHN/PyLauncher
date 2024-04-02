import json
from shutil import which
from datetime import datetime
from pathlib import Path
from modules.types import LauncherStandardConfigType, PyLauncherConfigType
from modules.variables import DEFAULT_LAUNCHER_PROFILES_CONFIG, \
    LAUNCHER_PROFILES_CONFIG_FILE, MINECRAFT_DIR, DEFAULT_JVM_FLAGS, \
    PYLAUNCHER_CONFIG_DIR, PYLAUNCHER_CONFIG_FILE, PYLAUNCHER_DEFAULT_CONFIG

class LauncherConfig:
    def __init__(self):
        lf = self.__open_file(LAUNCHER_PROFILES_CONFIG_FILE, DEFAULT_LAUNCHER_PROFILES_CONFIG)
        self.launcher_profiles_config: LauncherStandardConfigType = lf[1]
        self.launcher_profiles_file = lf[0]

        lpf = self.__open_file(PYLAUNCHER_CONFIG_FILE, PYLAUNCHER_DEFAULT_CONFIG)
        self.py_launcher_config: PyLauncherConfigType = lpf[1]
        self.py_launcher_file = lpf[0]

    def __open_file(self, file: Path, default):
        if file.exists() is False:
            file.parent.mkdir(parents=True, exist_ok=True)
            file2 = file.open("w+")
            json.dump(default, file2, indent=4)
            file2.seek(0)

            content = default
        else:
            file2 = file.open("r+")
            content = json.load(file2)

        return file2, content

    def add_profile(self, name, type, version, disable_chat=False, disable_multiplayer=False, gameDir=str(MINECRAFT_DIR), javaDir=which("java"), javaArgs=DEFAULT_JVM_FLAGS, resolution=None, icon="minecraft"):
        self["profiles"][name] = {
            "name": name,
            "type": type,
            "icon": icon,

            "created": datetime.now().isoformat(),
            "lastVersionId": version,

            "gameDir": gameDir,
            "javaDir": javaDir,
            "javaArgs": javaArgs,

            "disable_chat": disable_chat,
            "disable_multiplayer": disable_multiplayer,
        }

        if resolution is not None and isinstance(resolution, dict):
            self.launcher_profiles_config["profiles"][name]["resolution"] = resolution

    def remove_profile(self, name):
        del self.launcher_profiles_config["profiles"][name]

    def get_profile_names(self):
        return list(x["name"] for x in self.launcher_profiles_config["profiles"].values())

    def save(self):
        json.dump(self.launcher_profiles_config, self.launcher_profiles_file)
        json.dump(self.py_launcher_config, self.py_launcher_file)