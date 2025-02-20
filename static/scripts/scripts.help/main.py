from utils import lib, args

class HelpScriptArgumentParser(args.PrettyArgumentParser):
    def __init__(self, manifest: lib.Manifest):
        super().__init__(manifest = manifest)

    def options(self):
        return []

    def format_usage(self):
        return "u <script> [args...]"
    
    def print_help(self):
        print(f"User script manager and executor")
        print()
        self.print_usage()
        print()
        self.print_options()
        print()
        self.print_scripts()
        print()
        self.print_templates()

def main():
    manifest = lib.Manifest.load()
    parser = HelpScriptArgumentParser(manifest)
    parser.print_help()

if __name__ == "__main__":
    main()
