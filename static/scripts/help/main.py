from utils import lib, colors

def main():
    manifest = lib.Manifest.load()
    scripts = sorted(manifest.scripts, key=lambda x: x.name)

    print(f"User script manager and executor")
    print()
    print(f"{colors.GREEN}{colors.BOLD}Usage:{colors.ENDC} {colors.CYAN}u <script> [args...]{colors.ENDC}")
    print()
    print(f"{colors.GREEN}{colors.BOLD}Available scripts:{colors.ENDC}")

    descriptive_names = [script.name for script in scripts]
    len_of_longest_script_name = max([len(name) for name in descriptive_names])

    aliases = [', '.join(script.aliases) for script in scripts]
    len_of_longest_alias = max([len(alias) for alias in aliases])

    for (name, aliases, script) in zip(descriptive_names, aliases, scripts):
        alias_list = f"({aliases})" if aliases else ""
        print(
            f"  {colors.CYAN}{name}{colors.ENDC}",
            " " * (len_of_longest_script_name - len(name)),
            f"{colors.GRAY}{f'({aliases})' if aliases else '  '}{colors.ENDC}",
            " " * (len_of_longest_alias - len(aliases)),
            f"{script.description}"
        )

if __name__ == "__main__":
    main()
