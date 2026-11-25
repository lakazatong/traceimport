import os
import subprocess
import sys
from pathlib import Path
from subprocess import CalledProcessError


def main() -> int:
    try:
        separator = sys.argv.index("--")
    except ValueError:
        sys.exit("Usage: traceimport <package> -- <command> [args...]")

    if separator != 2 or separator == len(sys.argv) - 1:
        sys.exit("Usage: traceimport <package> -- <command> [args...]")

    target = sys.argv[1]
    command = sys.argv[separator + 1 :]

    package_dir = str(Path(__file__).parent)
    env = os.environ.copy()

    paths = env.get("PYTHONPATH", "").split(os.pathsep)
    env["PYTHONPATH"] = os.pathsep.join(
        [package_dir, *(path for path in paths if path)]
    )
    env["TRACEIMPORT_TARGET"] = target

    try:
        return subprocess.run(command, check=True, env=env).returncode
    except (FileNotFoundError, CalledProcessError):
        print(f"Command not found: {command[0]}", file=sys.stderr)
        return 127
