import argcomplete
import argparse
import importlib
import logging
import sys
import pkgutil
from functools import partial
from pathlib import Path

from project import Project


class Config:
    def __init__(self):
        this_file_path = Path(__file__)
        self.script_path = this_file_path.parent.resolve()

        self.projects = Config.get_projects()
        self.args: argparse.Namespace = None

    @staticmethod
    def get_projects():
        """Returns instances of all projects"""
        package_name = "projects"
        package = sys.modules[package_name]
        for _, name, _ in pkgutil.walk_packages(package.__path__):
            importlib.import_module(package_name + "." + name)

        projects = []
        for project_class in Project.get_subclasses():
            project_instance = project_class()
            projects.append(project_instance)
        return projects

    def parse_args(self):
        parser = argparse.ArgumentParser(
            prog="dev",
            description="Collection of useful commands for common dev tasks",
        )

        subparsers = parser.add_subparsers(dest="project", required=True)

        for project in self.projects:
            Config.add_project_parser(subparsers, project)

        argcomplete.autocomplete(parser)

        self.args = parser.parse_args()

    @staticmethod
    def add_project_parser(subparsers: argparse._SubParsersAction, project: Project):
        project_parser = subparsers.add_parser(project.name)
        command_subparsers = project_parser.add_subparsers(dest="command", required=True)
        for elem_name in dir(project.__class__):
            elem = getattr(project.__class__, elem_name)
            from project import command

            if isinstance(elem, command):
                command = getattr(project, elem_name)
                Config.add_command_parser(command_subparsers, project, command.method)

    @staticmethod
    def add_command_parser(
        command_subpasers: argparse._SubParsersAction,
        project: Project,
        func: classmethod,
    ):
        command_name = func.__name__
        command_parser: argparse.ArgumentParser = command_subpasers.add_parser(command_name)

        command_parser.set_defaults(func=partial(func, project))
        command_parser.description = func.__doc__

        for param_index, param_name in enumerate(func.__annotations__):
            Config.add_parser_argument(command_parser, func, param_index, param_name)

    @staticmethod
    def add_parser_argument(
        command_parser: argparse.ArgumentParser,
        func: classmethod,
        param_index,
        param_name: str,
    ):
        param_type = func.__annotations__[param_name]

        if param_type.__module__ != "builtins":
            help_message = param_type.__doc__
        else:
            help_message = param_type.__name__
        choices = Config.get_choices(param_type)

        arg_count = len(func.__annotations__)
        default_count = len(func.__defaults__) if func.__defaults__ else 0
        default_offset = arg_count - default_count

        if func.__defaults__ and param_index >= default_offset:
            default_index = param_index - default_offset
            param_default = func.__defaults__[default_index]
            help_message = f"{help_message} (default: {param_default})"
            command_parser.add_argument(
                f"--{param_name}",
                type=param_type,
                required=False,
                default=param_default,
                help=help_message,
            )
            default_index += 1
        else:
            command_parser.add_argument(
                param_name,
                type=param_type,
                help=help_message,
                choices=choices,
            )

    @staticmethod
    def get_choices(param_type):
        choices = None
        if hasattr(param_type, "__members__"):
            if param_type.__str__.__qualname__.startswith("Enum"):
                logging.warning(Config.suggestion_msg(param_type))
            choices = []
            for member in param_type.__members__:
                attr = getattr(param_type, member)
                choices.append(attr)
        return choices

    @staticmethod
    def suggestion_msg(param_type):
        param_type_name = param_type.__name__

        return f"""
Implement `__str__()` for `{param_type_name}` for a seamless integration with this script.

class {param_type_name}(Enum):
    Foo = "foo"
    Bar = "bar"

    def __str__(self):
        return self.value
"""

    def run_command(self):
        param_values = [getattr(self.args, param_name) for param_name in self.args.func.func.__annotations__]
        self.args.func(*param_values)
