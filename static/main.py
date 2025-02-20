#
# This is the main entry point for executing scripts. This script should dispatch out
# excution to scripts the user has create or builtin scripts.
#
# The CWD will be set to the directory containing this script by the parent process.
#

from typing import List
from utils import lib, colors

def exec(manifest: lib.Manifest, script_name: str, args: List[str]):
    script = manifest.get_script(script_name)
    if script is None:
        if script_name == "help":
            exit(2)
        else:
            print(f"{colors.BOLD}{colors.FAIL}[Error]{colors.ENDC} Script '{script_name}' not found.")
            print()
            exec(manifest, "help", [])
            exit(3)
    else:
        script.execute(args)

def main():
    args = lib.get_args()

    try:
        manifest = lib.Manifest.load()
    except:
        print(f"Unable to load manifest at {lib.manifest_path()}")
        exit(1)

    if len(args) == 0 or args[0] == "--help":
        exec(manifest, "help", [])
    else:
        exec(manifest, args[0], args[1:])

if __name__ == "__main__":
    main()
