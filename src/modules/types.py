from typing import TypedDict, Literal, Sequence, Optional

class EmptyDict(TypedDict):
    pass

class MinecraftResolution(TypedDict):
    width: int
    height: int
class ProfileType(TypedDict):
    name: str
    type: Literal["custom", "latest-release", "latest-snapshot"]

    allowedReleaseTypes: Optional[
        Sequence[
            Literal[
                "release", "snapshot", "beta", "alpha"
            ]
        ]
    ]

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

class User(TypedDict):
    displayName: str
    userid: str
    uuid: str
    username: str

class LauncherStandardConfigType(TypedDict):
    profiles: dict[str, ProfileType]
    authenticationDatabase: dict[str, User]

    launcher: PyLauncherConfigType

    clientToken: str

    selectedProfile: str
    selectedUser: str

    launcherVersion: LauncherVersionType