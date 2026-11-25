import atexit
import builtins
import os
import sys
import traceback

target = os.environ.get("TRACEIMPORT_TARGET")

if target:
    original_import = builtins.__import__
    found = False

    def traced_import(name, *args, **kwargs):
        global found

        if not found and (name == target or name.startswith(f"{target}.")):
            found = True
            print(f"\nFirst import of {target!r}: {name}", file=sys.stderr)
            traceback.print_stack(limit=30)

        return original_import(name, *args, **kwargs)

    def report() -> None:
        if not found:
            print(f"\n{target!r} was never imported.", file=sys.stderr)

    atexit.register(report)

    builtins.__import__ = traced_import
