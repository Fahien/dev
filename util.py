from pathlib import Path
import logging
import sys
import os
import subprocess
from log import Color


def get_workspace_path() -> Path:
    workspace_path_str = os.getenv("WORKSPACE_PATH")
    if workspace_path_str is None:
        logging.fatal("Please, specify a workspace directory with WORKSPACE_PATH environment variable")
        sys.exit(1)
    workspace_path = Path(workspace_path_str)
    if not workspace_path.exists():
        logging.fatal(f"{workspace_path_str} does not exist")
        sys.exit(1)
    return workspace_path


def run(command: list, cwd: Path = None):
    if cwd is not None and not cwd.exists():
        logging.fatal(f"{cwd} does not exist")

    command_msg = " ".join(map(str, command))
    logging.info(f"⏵ {command_msg}")
    subprocess.run(command, cwd=cwd)
