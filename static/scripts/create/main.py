from argparse import ArgumentParser, ArgumentError, ArgumentTypeError
from typing import List
from utils import lib, colors, args
from os import path
import re

EXPRESSION_REGEX = r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s*\}\}"

class CreateScriptArgumentParser(args.PrettyArgumentParser):
    def __init__(self, manifest: lib.Manifest):
        super().__init__(manifest = manifest)

    def options(self):
        return [
            ("--alias <alias>", "An alias for the script"),
            ("--description <description>", "A description for the script"),
            ("--template <template>", "The template to use"),
        ]

    def format_usage(self):
        return "u create <name>"
    
    def print_help(self):
        self.print_usage()
        print()
        self.print_options()
        print()
        self.print_templates()

def resolve(path: List[str], dict: dict) -> any:
    if not path:
        return None

    for key in path:
        if key not in dict:
            return None
        dict = dict[key]

    return dict

def interpolate(template: str, args: dict) -> str:
    while match := re.search(EXPRESSION_REGEX, template):
        path = match.group(1).split('.')
        value = resolve(path, args)
        if value is not None:
            template = template.replace(match.group(0), value)
    return template

def deep_interpolate(obj: dict, args: dict) -> dict:
    for key, value in obj.items():
        if isinstance(value, str):
            obj[key] = interpolate(value, args)
        elif isinstance(value, list):
            obj[key] = [interpolate(item, args) for item in value]
        elif isinstance(value, dict):
            obj[key] = deep_interpolate(value, args)
    return obj

def to_safe_filename(input_str: str) -> str:
    input_str = input_str.strip()
    input_str = input_str.replace(' ', '_')
    input_str = input_str.replace('/', '.')
    safe_filename = re.sub(r'[^a-zA-Z0-9-_\.]', '', input_str).lower()
    if not safe_filename:
        print(f"{colors.FAIL}[Error]{colors.ENDC} Invalid script name '{input_str}'")

    return safe_filename

def main():
    manifest = lib.Manifest.load()
    parser = CreateScriptArgumentParser(manifest)
    parser.add_argument("--alias", action='append', default=[])
    parser.add_argument("--description")
    parser.add_argument("--template", default="sh")
    parser.add_argument("name")

    args = parser.parse_args(lib.get_args())
    template = manifest.get_template(args.template)

    if not template:
        print(f"{colors.FAIL}[Error]{colors.ENDC} Template '{args.template}' not found")
        print()
        parser.print_templates()
        exit(1)

    script_dir = path.join("scripts", to_safe_filename(args.name))
    script_abs_dir = path.join(lib.get_cwd(), script_dir)

    # Error if script directory already exists
    if path.exists(script_dir):
        print(f"{colors.FAIL}[Error]{colors.ENDC} Script '{args.name}' already exists at '{script_abs_dir}'")
        exit(1)

    # Error if the source template directory does not exist
    if not path.exists(template.path):
        print(f"{colors.FAIL}[Error]{colors.ENDC} Template '{args.template}' not found at '{template.path}'")
        exit(1)

    template_clone = template.template.copy()
    script = deep_interpolate(template_clone, {
        "script": { 
            "dir": script_dir,
            "name": args.name,
        }
    })

    script["name"] = args.name
    script["path"] = script_dir

    if args.description:
        script["description"] = args.description

    if args.alias:
        script["aliases"] = args.alias

    manifest.add_script(lib.Script.parse_from(script))
    manifest.save()

    # Copy the template directory to the new script directory
    if lib.copy_dir(template.path, script_abs_dir) != 0:
        print(f"{colors.FAIL}[Error]{colors.ENDC} Failed to copy template to '{script_abs_dir}'")
        exit(1)

    print("Script:", script)

if __name__ == "__main__":
    main()
