import sys

from src.backend.style import Logger
from src.backend.utils import check_call

from src.backend.run_utils import ResourcesFile, GetUiFiles, UI_DIR, BLP_DIR, \
    BLP_FILES

res = ResourcesFile()
check_call("blueprint-compiler", "batch-compile", UI_DIR, BLP_DIR, *BLP_FILES, can_exit=True, buffer=sys.stdout)

for x in GetUiFiles():
    res.append(x)
    
res.save()
res.compile()

# Logger.error(res.items)

Logger.info("Notes:")
print("\t• If the libadwaita stylesheet not applying, it should be a problem related to callbacks")

check_call("python3", "main.py", wd="src", buffer=sys.stdout, can_exit=True)