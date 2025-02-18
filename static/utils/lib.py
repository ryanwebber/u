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

class Script:
    def __init__(self, name: str, description: str, cmd: str, args: List[str], aliases: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.cmd = cmd
        self.args = args
        self.aliases = aliases or []

    def __repr__(self):
        return f"Script(name={self.name}, description={self.description}, cmd={self.cmd}, args={self.args}, aliases={self.aliases})"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "cmd": self.cmd,
            "args": self.args,
            "aliases": self.aliases
        }

    def execute(self, args: List[str]):
        subprocess.run(self.cmd.split(' ') + self.args + args)

class Template:
    def __init__(self, name: str, description: str, path: str, cmd: str, args: List[str]):
        self.name = name
        self.description = description
        self.path = path
        self.cmd = cmd
        self.args = args

    def __repr__(self):
        return f"Template(name={self.name}, description={self.description}, path={self.path}, cmd={self.cmd}, args={self.args})"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "path": self.path,
            "template": {
                "cmd": self.cmd,
                "args": self.args
            }
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
            Script(
                name=script['name'],
                description=script['description'],
                cmd=script['cmd'],
                args=script['args'],
                aliases=script.get('aliases')
            ) for script in data.get('scripts', [])
        ]
        
        # Decode templates
        templates = [
            Template(
                name=template['name'],
                description=template['description'],
                path=template['path'],
                cmd=template['template']['cmd'],
                args=template['template']['args']
            ) for template in data.get('templates', [])
        ]
        
        # Create and return the Manifest object
        return Manifest(scripts=scripts, templates=templates)

    def get_script(self, name: str) -> Optional[Script]:
        for script in self.scripts:
            if script.name == name or name in script.aliases:
                return script
        return None
