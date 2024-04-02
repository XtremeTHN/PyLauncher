from typing import TypedDict, Literal, Sequence


class MinecraftResolution(TypedDict):
    width: int
    height: int
class ProfileType(TypedDict):
    name: str
    type: Literal["custom", "latest-release", "latest-snapshot"]

    created: str
    icon: str

    lastVersionId: str
    gameDir: str

    javaDir: str
    javaArgs: Sequence[str]

    resolution: MinecraftResolution
    disable_chat: bool
    disable_multiplayer: bool

class PyLauncherConfigType(TypedDict):
    doAfterLaunch: Literal["close", "minimize", "stayOpen"]
    show_snapshots: bool
    show_beta_versions: bool
    show_alpha_versions: bool

class LauncherVersionType(TypedDict):
    name: str
    format: int
    profilesFormat: int

class AuthenticationDatabaseType(TypedDict):
    displayName: str
    userid: str
    uuid: str
    username: str

class LauncherStandardConfigType(TypedDict):
    profiles: dict[str, ProfileType]
    authenticationDatabase: dict

    launcher: PyLauncherConfigType

    selectedUser: str

    launcherVersion: LauncherVersionType