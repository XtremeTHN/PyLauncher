from minecraft_launcher_lib.install import install_minecraft_version
from minecraft_launcher_lib.utils import get_latest_version, generate_test_options
from minecraft_launcher_lib.command import get_minecraft_command

import os

latest = get_latest_version()["release"]

# install_minecraft_version(latest, os.path.expanduser("~/.minecraft"), callback={
#     "setProgress": print
# })

options = generate_test_options()
print(options)
minecraft_cmd = get_minecraft_command(latest, os.path.expanduser("~/.minecraft"), options)

print(minecraft_cmd)
# os.system(" ".join(minecraft_cmd))