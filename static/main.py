#
# This is the main entry point for executing scripts. This
# script should dispatch out excution to scripts the user
# has create or builtin scripts.
#
# The CWD will be set to the directory containing this script 
# by the parent process.
#

import sys
import os

print("Cwd:", os.getcwd())
print("Args:", *sys.argv[1:])
