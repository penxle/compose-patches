import json
import sys
from pathlib import Path


def verification_arguments(commands):
    tasks = {}
    for command in commands:
        if (
            not command
            or not command[0].startswith(":")
            or len(command) % 2 != 1
            or any(option != "--tests" for option in command[1::2])
        ):
            raise ValueError(f"Expected one task followed by --tests PATTERN pairs: {command!r}")

        task = command[0]
        tasks.setdefault(task, set())
        if len(command) == 1:
            # An unfiltered invocation already covers every requested test pattern.
            tasks[task] = None
        elif tasks[task] is not None:
            tasks[task].update(command[2::2])

    arguments = []
    for task, patterns in tasks.items():
        arguments.append(task)
        for pattern in sorted(patterns or []):
            arguments.extend(["--tests", pattern])
    if not arguments:
        raise ValueError("No verification tasks were specified")
    return arguments


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    release = json.loads((root / "releases" / sys.argv[1] / "release.json").read_text())
    commands = []
    for patch_id in release["patches"]:
        manifest = json.loads((root / "patches" / patch_id / "patch.json").read_text())
        commands.extend(manifest["verify_commands"])
    print(json.dumps(verification_arguments(commands)))
