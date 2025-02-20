from utils import lib, colors, args
from os import path, environ
import subprocess

class EditScriptArgumentParser(args.PrettyArgumentParser):
    def __init__(self, manifest: lib.Manifest):
        super().__init__(manifest = manifest)

    def options(self):
        return [
            ("--editor <editor>", "A program to open the script with"),
        ]

    def format_usage(self):
        return "u edit <name>"
    
    def print_help(self):
        self.print_usage()
        print()
        self.print_options()
        print()
        self.print_scripts()

def main():
    manifest = lib.Manifest.load()
    parser = EditScriptArgumentParser(manifest)
    parser.add_argument("name")
    parser.add_argument("--editor", default=environ.get("EDITOR"))

    args = parser.parse_args(lib.get_args())
    if args.editor is None:
        print(f"{colors.FAIL}[Error]{colors.ENDC} No editor specified. Set the EDITOR environment variable or use the --editor flag.")
        exit(1)

    script = manifest.get_script(args.name)
    if script is None:
        print(f"{colors.BOLD}{colors.FAIL}[Error]{colors.ENDC} Script '{args.name}' not found.")
        print()
        parser.print_scripts()
        exit(3)

    subprocess.run([args.editor, path.join(lib.get_cwd(), script.path)])

if __name__ == "__main__":
    main()
