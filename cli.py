import turing
import argparse
from pathlib import Path

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path of json file")
    parser.add_argument("index", help="Index tape", type=int)
    args = parser.parse_args()

    target_dir = Path(args.path)

    if not target_dir.exists():
        parser.exit(1, message="The target directory doesn't exist")

    tm, tapes = turing.read_json_machine_config(args.path)

    if tapes is not None and tm is not None:
        if args.index < len(tapes):
            run_ok = tapes[args.index].run(tm)
            if not run_ok:
                parser.exit(1, message=f"Unexpected value in instructions")
        else:
            parser.exit(1, message=f"This file has {len(tapes)} tapes try an index lower than that")
    else:
        parser.exit(1, message="The target directory has some error")

if __name__ == "__main__":
    cli()
