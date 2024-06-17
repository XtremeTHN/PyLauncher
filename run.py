import sys

from src.modules.style import Logger
from src.modules.utils import check_call

from src.modules.run_utils import ResourcesFile, UI_DIR, BLP_DIR, \
    BLP_FILES, UI_FILES

res = ResourcesFile()
check_call("blueprint-compiler", "batch-compile", UI_DIR, BLP_DIR, *BLP_FILES, can_exit=True, buffer=sys.stdout)

for x in UI_FILES:
    res.append(x)
    
res.save()
res.compile()

Logger.info("Notes:")
print("\t• If the libadwaita stylesheet not applying, it should be a problem related to callbacks")

check_call("python3", "main.py", wd="src", buffer=sys.stdout, can_exit=True)