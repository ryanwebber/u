import json
import os
import sys
import subprocess
from typing import Self, List, Optional

def get_args() -> list[str]:
    return sys.argv[1:]

def get_cwd() -> str:
    return os.getcwd()

def manifest_path() -> str:
    return os.path.join(get_cwd(), "manifest.json")

def copy_dir(src: str, dest: str) -> int:
    # Copy, preserving symbolic links, and return the exit code
    if sys.platform == "darwin":
        return subprocess.run(["cp", "-r", "-P", src, dest]).returncode
    else:
        return subprocess.run(["cp", "-r", "-a", src, dest]).returncode

def delete_dir(path: str) -> int:
    # Delete the directory and return the exit code
    return subprocess.run(["rm", "-rf", path]).returncode

class Script:
    def __init__(self, name: str, path: str, cmd: str, args: List[str], description: Optional[str] = None, aliases: Optional[List[str]] = None):
        self.name = name
        self.path = path
        self.description = description
        self.cmd = cmd
        self.args = args
        self.aliases = aliases or []

    def __repr__(self):
        return f"Script(name={self.name}, path={self.path}, description={self.description}, cmd={self.cmd}, args={self.args}, aliases={self.aliases})"

    def to_dict(self):
        dict = {
            "name": self.name,
            "path": self.path,
            "description": self.description,
            "cmd": self.cmd,
            "args": self.args,
            "aliases": self.aliases
        }

        return {k: v for k, v in dict.items() if v}
    
    @staticmethod
    def parse_from(data: dict) -> Self:
        script = Script(
            name=data['name'],
            path=data['path'],
            cmd=data['cmd'],
            args=data['args'] or [],
        )

        if 'description' in data:
            script.description = data['description']

        if 'aliases' in data:
            script.aliases = data['aliases']

        return script

    def execute(self, args: List[str]):
        subprocess.run(self.cmd.split(' ') + self.args + args)

class Template:
    def __init__(self, name: str, description: str, path: str, template: dict):
        self.name = name
        self.description = description
        self.path = path
        self.template = template

    def __repr__(self):
        return f"Template(name={self.name}, description={self.description}, path={self.path}, template={self.template})"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "path": self.path,
            "template": self.template
        }

class Manifest:
    def __init__(self, scripts: List[Script], templates: List[Template]):
        self.scripts = scripts
        self.templates = templates

    def __repr__(self):
        return f"Manifest(scripts={self.scripts}, templates={self.templates})"

    def to_dict(self):
        return {
            "scripts": [script.to_dict() for script in self.scripts],
            "templates": [template.to_dict() for template in self.templates]
        }

    def save(self):
        with open(manifest_path(), 'w') as file:
            json.dump(self.to_dict(), file, indent=4)
    
    @staticmethod
    def load() -> Self:
        try:
            with open(manifest_path(), 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("No manifest file found at ", manifest_path())
            exit(1)
 
        return Manifest.parse_from(data)

    @staticmethod
    def parse_from(data: any) -> Self:
        
        # Decode scripts
        scripts = [
            Script.parse_from(script) for script in data.get('scripts', [])
        ]
        
        # Decode templates
        templates = [
            Template(
                name=template['name'],
                description=template['description'],
                path=template['path'],
                template=template['template']
            ) for template in data.get('templates', [])
        ]
        
        # Create and return the Manifest object
        return Manifest(scripts=scripts, templates=templates)

    def get_script(self, name: str) -> Optional[Script]:
        for script in self.scripts:
            if script.name == name or name in script.aliases:
                return script
        return None
    
    def add_script(self, script: Script):
        self.scripts.append(script)

    def remove_script(self, name: str):
        self.scripts = [script for script in self.scripts if script.name != name]
    
    def get_template(self, name: str) -> Optional[Template]:
        for template in self.templates:
            if template.name == name:
                return template
        return None
    
    def add_template(self, template: Template):
        self.templates.append(template)
