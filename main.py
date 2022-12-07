import turing

tm, tapes = turing.read_json_machine_config("./examples/binary-increment.json")

if tapes is not None and tm is not None:
    tapes[1].run(tm)
