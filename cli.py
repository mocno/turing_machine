"""This is a cli of a turing machine, with a simple tape or a '2d tape'"""

import argparse
import time
from pathlib import Path

import turing
from turing import JSONDecodeError, UnexpectedState

ERASE_LINE = '\033[2K'
CURSOR_UP = '\033[F'

def cli():
    """This is a cli function of a turing machine, with a simple tape or a '2d tape'"""

    parser = argparse.ArgumentParser(
        description='Simulate a turing machine, with a simple tape or a "2d tape"')

    parser.add_argument("path",
        help="Path of json file. For more information, you can see the README and the examples")
    parser.add_argument("index", help="Index tape", type=int)
    parser.add_argument("-d", "--delay", help="Delay in each step", type=float, default=.3)
    args = parser.parse_args()

    target_dir = Path(args.path)

    if not target_dir.exists():
        parser.exit(1, message="The target directory doesn't exist")

    try:
        machine = turing.parse_json_machine(args.path)
    except JSONDecodeError:
        parser.exit(1, message="The target file has some error")
    except UnexpectedState as e:
        parser.exit(1, message=f"Unexpected start state: {e}")

    try:
        tape = machine.tapes[args.index]
    except IndexError:
        parser.exit(1, message=
            f"This file has {len(machine.tapes)} tapes try an index lower than that")

    while True:
        _continue = machine.step(tape)

        if tape.type == 'tape':
            print(ERASE_LINE + machine.state)
            print(ERASE_LINE)
            print(str(tape) + CURSOR_UP * 2)
        elif tape.type == '2d':
            print(ERASE_LINE + machine.state)
            print(ERASE_LINE)
            print(str(tape) + CURSOR_UP * (2+str(tape).count('\n')))

        if not _continue:
            break

        time.sleep(args.delay)

if __name__ == "__main__":
    cli()
