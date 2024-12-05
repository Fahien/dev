from enum import Enum
from functools import reduce
from pathlib import Path

import util


class BuildType(Enum):
    DEBUG = "debug"
    RELEASE = "release"

    def __str__(self):
        return self.value


class DerivationRegistry(type):
    def __init__(cls, name, bases, cls_dict):
        type.__init__(cls, name, bases, cls_dict)
        cls._subclasses = set()
        for base in bases:
            if isinstance(base, DerivationRegistry):
                base._subclasses.add(cls)

    def get_subclasses(cls):
        return reduce(
            set.union,
            (succ.get_subclasses() for succ in cls._subclasses if isinstance(succ, DerivationRegistry)),
            cls._subclasses,
        )


class command:
    def __init__(self, m):
        self.method = m


class Project(metaclass=DerivationRegistry):
    name: str
    project_path: Path

    def __init__(self, name: str):
        self.name = name
        self.project_path = util.get_workspace_path().joinpath(name)
        self.build_path = self.project_path.joinpath("build")
        self.install_path = self.build_path.joinpath("install")
