import json
import uuid
import traceback

from shutil import which
from datetime import datetime
from pathlib import Path

from modules.types import LauncherStandardConfigType, PyLauncherConfigType, User, ProfileType, EmptyDict
from modules.variables import DEFAULT_LAUNCHER_PROFILES_CONFIG, \
    LAUNCHER_PROFILES_CONFIG_FILE, MINECRAFT_DIR, DEFAULT_JVM_FLAGS, \
    PYLAUNCHER_CONFIG_DIR, PYLAUNCHER_CONFIG_FILE, PYLAUNCHER_DEFAULT_CONFIG

from gi.repository import GObject 

class LauncherConfig(GObject.GObject):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ())
    }
    def __init__(self):
        super().__init__()
        self.launcher_profiles_config: LauncherStandardConfigType = self.__open_file(LAUNCHER_PROFILES_CONFIG_FILE,
                                                                                     DEFAULT_LAUNCHER_PROFILES_CONFIG)

        self.py_launcher_config: PyLauncherConfigType = self.__open_file(PYLAUNCHER_CONFIG_FILE, 
                                                                         PYLAUNCHER_DEFAULT_CONFIG)

    def __open_file(self, file: Path, default):
        if file.exists() is False:
            file.parent.mkdir(parents=True, exist_ok=True)
            with open(str(file), 'w') as file_obj:
                json.dump(default, file_obj, indent=4)

            content = default
        else:
            with open(str(file), 'r') as file_obj:
                content = json.load(file_obj)

        return content

    def add_profile(self, name, type, version, disable_chat=False, disable_multiplayer=False, gameDir=str(MINECRAFT_DIR), javaDir=which("java"), javaArgs=DEFAULT_JVM_FLAGS, resolution=None, icon="minecraft"):
        self.launcher_profiles_config["profiles"][name] = {
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
        
        self.save()
    
    def add_profile_dict(self, name: str, config: ProfileType):
        self.launcher_profiles_config["profiles"][name] = config
        self.save()

    def remove_profile(self, name, save=True):
        del self.launcher_profiles_config["profiles"][name]
        if save is True:
            self.save()
        
    def get_profile(self, name) -> ProfileType | EmptyDict:
        return self.launcher_profiles_config["profiles"].get(name, {})

    def get_user(self, _uuid) -> User | EmptyDict:
        return self.launcher_profiles_config["authenticationDatabase"][_uuid]

    def get_selected_profile(self) -> ProfileType | EmptyDict:
        return self.launcher_profiles_config.get("profiles", {}).get(self.launcher_profiles_config.get("selectedProfile", ""), {})
    
    def get_profiles_names(self) -> list[str]:
        return list(x["name"] for x in self.launcher_profiles_config["profiles"].values())

    def get_profiles_key_names(self) -> list[str]:
        return list(self.launcher_profiles_config["profiles"].keys())
        
    def get_profiles(self) -> list[ProfileType]:
        return self.launcher_profiles_config["profiles"]

    def get_selected_user(self) -> User | EmptyDict:
        return self.launcher_profiles_config.get("authenticationDatabase", {}).get(self.launcher_profiles_config.get("selectedUser", ""), {})

    def set_selected_profile(self, name):
        self.launcher_profiles_config["selectedProfile"] = name
        self.save()

    def set_selected_user(self, _uuid):
        self.launcher_profiles_config["selectedUser"] = _uuid
        self.save()

    def add_user(self, name) -> str:
        """Adds a user to the authentication database

        Args:
            name (str): The name of the user

        Returns:
            str: The uuid of the user
        """

        str_uuid = str(uuid.uuid4())
        self.launcher_profiles_config["authenticationDatabase"][str_uuid] = {
            "displayName": name,
            "userid": name,
            "uuid": str_uuid,
            "username": name
        }
        self.save()

        return str_uuid
    
    def set_selected_user(self, name):
        """Sets the selected profile.

        Args:
            name (str): The uuid of the user
        """
        self.launcher_profiles_config["selectedUser"] = name
        self.save()

    def save(self):
        with open(LAUNCHER_PROFILES_CONFIG_FILE, "w") as f:
            json.dump(self.launcher_profiles_config, f, indent=4)

        with open(PYLAUNCHER_CONFIG_FILE, "w") as f:
            json.dump(self.py_launcher_config, f, indent=4)
        self.emit('changed')
