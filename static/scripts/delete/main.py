from utils import lib, colors, args
from os import path

class DeleteScriptArgumentParser(args.PrettyArgumentParser):
    def __init__(self, manifest: lib.Manifest):
        super().__init__(manifest = manifest)

    def options(self):
        return []

    def format_usage(self):
        return "u delete <name>"
    
    def print_help(self):
        self.print_usage()
        print()
        self.print_options()
        print()
        self.print_scripts()

def main():
    manifest = lib.Manifest.load()
    parser = DeleteScriptArgumentParser(manifest)
    parser.add_argument("name")

    args = parser.parse_args(lib.get_args())
    script = manifest.get_script(args.name)

    if script is None:
        print(f"{colors.BOLD}{colors.FAIL}[Error]{colors.ENDC} Script '{args.name}' not found.")
        print()
        parser.print_help()
        exit(3)

    script_abs_path = path.join(lib.get_cwd(), script.path)
    
    if lib.delete_dir(script.path) != 0:
        print(f"{colors.FAIL}[Error]{colors.ENDC} Failed to delete script '{args.name}' at '{script_dir}'")
        exit(1)

    manifest.remove_script(args.name)
    manifest.save()

    print(f"Deleted script '{colors.GREEN}{args.name}{colors.ENDC}' at {colors.GRAY}{script_abs_path}{colors.ENDC}")

if __name__ == "__main__":
    main()
