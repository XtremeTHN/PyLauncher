import json
from modules.variables import DEFAULT_LAUNCHER_CONFIG, LAUNCHER_CONFIG_FILE

class LauncherConfig(dict):
    def __init__(self):
        config = DEFAULT_LAUNCHER_CONFIG
        
        if LAUNCHER_CONFIG_FILE.exists() is False:
            # LAUNCHER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            self.file = LAUNCHER_CONFIG_FILE.open("w+")
            json.dump(config, self.file, indent=4)
        else:
            self.file = LAUNCHER_CONFIG_FILE.open("r+")
        
        self.file.seek(0)
        config = json.load(self.file)

        super().__init__(config)
    
    def add_profile(self, name, version, jvm_flags, java_bin_path, minecraft_root_path, resolution, disable_chat, disable_multiplayer):
        self["profiles"][name] = {
            "version": version,
            "jvm-flags": jvm_flags,
            "java-bin-path": java_bin_path,
            "minecraft-root-path": minecraft_root_path,
            "resolution": resolution,
            "disable-chat": disable_chat,
            "disable-multiplayer": disable_multiplayer
        }

    def remove_profile(self, name):
        del self["profiles"][name]

    def get_profile_names(self):
        return list(x["name"] for x in self["profiles"].values())

    def save(self):
        json.dump(self, self.file)
