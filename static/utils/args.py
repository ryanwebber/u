from argparse import ArgumentParser
from typing import List
from . import lib, colors

class PrettyArgumentParser(ArgumentParser):
    def __init__(self, manifest: lib.Manifest):
        super().__init__(exit_on_error=False)
        self.manifest = manifest

    def options(self) -> List[tuple[str, str]]:
        """
        Returns a list of tuples representing the options for the script and their description
        """

    def format_usage(self):
        """
        Returns a string representing the usage of the script
        """

    def print_help(self):
        """
        Prints the format of the script
        """
        self.print_usage()
        print()
        self.print_options()
    
    def print_usage(self, file = None):
        print(f"{colors.GREEN}{colors.BOLD}Usage:{colors.ENDC} {colors.CYAN}{self.format_usage()}{colors.ENDC}")
    
    def print_options(self, file = None):
        print(f"{colors.GREEN}{colors.BOLD}Options:{colors.ENDC}")

        options = self.options()
        if not options:
            print(f"    --help  Print this help message and exit")
            return

        len_of_longest_option = max([len(option[0]) for option in options])
        for option, description in options:
            print(
                f"    {option}",
                " " * (len_of_longest_option - len(option)),
                f"{description}"
            )
        
    def print_templates(self):
        templates = sorted(self.manifest.templates, key=lambda x: x.name)
        template_names = [template.name for template in templates]
        len_of_longest_template_name = max([len(name) for name in template_names])

        print(f"{colors.GREEN}{colors.BOLD}Available templates:{colors.ENDC}")
        for template in templates:
            print(
                f"  {colors.CYAN}{template.name}{colors.ENDC}",
                " " * (len_of_longest_template_name - len(template.name)),
                f"{template.description}"
            )
        
    def print_scripts(self):
        scripts = sorted(self.manifest.scripts, key=lambda x: x.name)
        descriptive_names = [script.name for script in scripts]
        len_of_longest_script_name = max([len(name) for name in descriptive_names])

        aliases = [', '.join(script.aliases) for script in scripts]
        len_of_longest_alias = max([len(alias) for alias in aliases])

        print(f"{colors.GREEN}{colors.BOLD}Available scripts:{colors.ENDC}")
        for (name, aliases, script) in zip(descriptive_names, aliases, scripts):
            print(
                f"  {colors.CYAN}{name}{colors.ENDC}",
                " " * (len_of_longest_script_name - len(name)),
                f"{colors.GRAY}{f'({aliases})' if aliases else '  '}{colors.ENDC}",
                " " * (len_of_longest_alias - len(aliases)),
                f"{script.description}"
            )

    def error(self, message):
        if message:
            print(f"{colors.BOLD}{colors.FAIL}[Error]{colors.ENDC} {message}")
            print()

        self.print_help()
        exit(1)
