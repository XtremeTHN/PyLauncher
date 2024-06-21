import sys

from pylauncher.backend.style import Logger
from pylauncher.backend.utils import check_call

from pylauncher.backend.run_utils import ResourcesFile, GetUiFiles, UI_DIR, BLP_DIR, \
    BLP_FILES

res = ResourcesFile()
check_call("blueprint-compiler", "batch-compile", UI_DIR, BLP_DIR, *BLP_FILES, can_exit=True, buffer=sys.stdout)

for x in GetUiFiles():
    res.append(x)
    
res.save()
res.compile()

Logger.info("Notes:")
print("\t• If the libadwaita stylesheet not applying, it should be a problem related to callbacks")

# check_call("python3", "main.py", wd="pylauncher", buffer=sys.stdout, can_exit=True)
from pylauncher.main import main

sys.exit(main())