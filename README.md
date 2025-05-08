# Dev

A Python framework for managing development tasks across projects.

- Organizes commands by project namespace
- Provides automatic command-line argument parsing based on function annotations
- Supports tab completion for commands and arguments
- Includes colorized logging output
- Makes it easy to extend with new projects and commands

## Installation

Prerequisites:
- Python 3.x
- `argcomplete` package for command completion

## Setup

1. Clone the repository in your _dev-main_ directory or add it as a git submodule:
   ```console
   git clone https://github.com/fahien/dev.git

   # or
   git submodule add https://github.com/fahien/dev.git
   ```

2. Install `argcomplete`:
   ```console
   pip install argcomplete
   ```

3. Enable global completion:
   ```console
   activate-global-python-argcomplete --user
   ```

4. Add to your shell configuration (e.g., `.bashrc` or `.zshrc`):
   ```sh
   # Root directory for all projects (required)
   export WORKSPACE_PATH="/path/to/your/workspace"

   DEV_PATH="$WORKSPACE_PATH/dev-main/main.py"
   eval "$(register-python-argcomplete $DEV_PATH)"
   alias dev="$DEV_PATH"
   ```

## Usage

Run commands with the following structure:

```console
dev <project-name> <command> [arguments]
```

Example:

```console
dev myproject build --config release
```

## Project Structure

- `__init__.py` - Sets up imports
- `config.py` - Handles command-line parsing
- `log.py` - Implements colored logging
- `project.py` - Defines the base Project class
- `util.py` - Provides utility functions

## Creating New Projects

1. Create a new Python file in the `dev-main/projects` directory
2. Define a class that extends `Project` from the `projects` module
3. Add methods decorated with `@command` for each method that you want to be exposed to the CLI

Example:

```py
from enum import Enum
from project import Project, command, BuildType
import util

class MyProject(Project):
    def __init__(self):
        Project.__init__(self, "myproject")  # This sets the project name for CLI

    @command
    def build(self, config: BuildType = BuildType.DEBUG):
        """Build the project with specified configuration."""
        util.run(["make", f"CONFIG={config}"], cwd=self.project_path)

    @command
    def clean(self):
        """Clean build artifacts."""
        util.run(["make", "clean"], cwd=self.project_path)
```

## Features

- Commands can use type annotations to define the values expected through the CLI:
  ```py
  @command
  def deploy(self, target: str, verbose: bool = False):
      """Deploy to specified target."""
      # Implementation here
  ```
  Will yield:
  ```console
  $ dev myproject deploy --help
  usage: dev myproject deploy [-h] [--verbose VERBOSE] target
  
  Deploy to specified target.
  
  positional arguments:
    target                str
  
  optional arguments:
    -h, --help           show this help message and exit
    --verbose VERBOSE    bool (default: False)
  ```

- Enum types are automatically converted to command-line choices via the `__str__` method:
  ```py
  class Platform(Enum):
      LINUX = "linux"
      MACOS = "macos"
      WINDOWS = "windows"

      def __str__(self):
          return self.value

  @command
  def build_for(self, platform: Platform):
      """Build for specific platform."""
      # Implementation
  ```
  Will yield:
  ```console
  $ dev myproject build_for --help
  usage: dev myproject build_for [-h] {linux,macos,windows}
  
  Build for specific platform.
  
  positional arguments:
    {linux,macos,windows}
  
  optional arguments:
    -h, --help            show this help message and exit
  ```

- Default values for optional arguments:
  ```py
  @command
  def build(self, config: BuildType = BuildType.DEBUG):
      """Build the project with specified configuration."""
      util.run(["make", f"CONFIG={config}"], cwd=self.project_path)
  ```
  Will yield:
  ```console
  $ dev myproject build --help
  usage: dev myproject build [-h] [--config {debug,release}]
  
  Build the project with specified configuration.
  
  optional arguments:
    -h, --help            show this help message and exit
    --config {debug,release}
                          None (default: debug)
  ```

- Use the built-in colored logging:
  ```py
  import logging

  logging.info("Starting build process...")
  logging.warning("Configuration file not found")
  logging.error("Build failed")
  ```

## License

Dual licensed under either
- [MIT License](LICENSE-MIT)
- [Apache License, Version 2.0](LICENSE-APACHE)

## Contributing

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.
