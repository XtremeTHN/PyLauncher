from typing import TypedDict, Literal, Sequence, Optional


class MinecraftResolution(TypedDict):
    width: int
    height: int
class ProfileType(TypedDict):
    name: str
    type: Literal["custom", "latest-release", "latest-snapshot"]

    created: str
    icon: Optional[str]

    lastVersionId: str
    gameDir: Optional[str]

    javaDir: Optional[str]
    javaArgs: Optional[Sequence[str]]

    resolution: Optional[MinecraftResolution]
    disable_chat: bool
    disable_multiplayer: bool

class PyLauncherConfigType(TypedDict):
    doAfterLaunch: Literal["close", "minimize", "stayOpen"]

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
    authenticationDatabase: AuthenticationDatabaseType

    launcher: PyLauncherConfigType

    clientToken: str

    selectedProfile: str
    selectedUser: str

    launcherVersion: LauncherVersionType