#
# This is the main entry point for executing scripts. This script should dispatch out
# excution to scripts the user has create or builtin scripts.
#
# The CWD will be set to the directory containing this script  by the parent process.
#

import utils.lib

def main():
    manifest = utils.lib.Manifest.load()
    print(manifest)

if __name__ == "__main__":
    main()
