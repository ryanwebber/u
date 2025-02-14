import json
import os
import sys
from typing import Self, List, Optional

def args() -> list[str]:
    return sys.argv[1:]

def cwd() -> str:
    return os.getcwd()

def manifest_path() -> str:
    return os.path.join(os.getcwd(), "manifest.json")

class Script:
    def __init__(self, name: str, description: str, cmd: str, args: List[str], aliases: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.cmd = cmd
        self.args = args
        self.aliases = aliases or []  # Default to empty list if None

    def __repr__(self):
        return f"Script(name={self.name}, description={self.description}, cmd={self.cmd}, args={self.args}, aliases={self.aliases})"


class Template:
    def __init__(self, name: str, description: str, path: str, cmd: str, args: List[str]):
        self.name = name
        self.description = description
        self.path = path
        self.cmd = cmd
        self.args = args

    def __repr__(self):
        return f"Template(name={self.name}, description={self.description}, path={self.path}, cmd={self.cmd}, args={self.args})"


class Manifest:
    def __init__(self, scripts: List[Script], templates: List[Template]):
        self.scripts = scripts
        self.templates = templates

    def __repr__(self):
        return f"Manifest(scripts={self.scripts}, templates={self.templates})"
    
    @staticmethod
    def load() -> Self:
        with open(manifest_path(), 'r') as file:
            data = json.load(file)
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
                aliases=script.get('aliases')  # Optional field
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
