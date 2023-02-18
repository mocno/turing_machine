"""Simulates a turing machine, with a simple tape or a '2d tape'"""

class JSONDecodeError(ValueError):
    """Error on decode json, unexpected format"""

class UnexpectedState(ValueError):
    """Unexpected state, state out of states"""

class UnexpectedDirection(ValueError):
    """Unexpected direction, instruction with some direction error"""

import json

class Instruction:
    pass

class TapeMixin:
    pass

class Tape(TapeMixin):
    pass

class Tape2d(TapeMixin):
    pass

class MachineConfiguration:
    pass

class Machine:
    pass


def parse_json_machine(filepath: str, encoding: str = "utf-8") -> Machine:
    """Parse from a json file configurations of a turing machine"""

    with open(filepath, 'r', encoding=encoding) as file:
        data = file.read()

    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError as exception:
        raise JSONDecodeError("The file has some json error") from exception

    return generate_machine_from_dict(data)

def generate_machine_from_dict(data: dict):
    """Generate a turing machine by dict"""

    states = data['states']
    start_state = data['start-state']
    else_sign: str|None = data.get('else-sign', None)

    configuration = MachineConfiguration(states, start_state, else_sign)

    blank_symbol = data.get('blank-symbol', ' ')

    try:
        inputs: List[dict[str, str|List[int]]] = data['inputs']
    except KeyError:
        return Machine(configuration, [])

    tapes: List[TapeMixin] = []

    # types: tape, 2d, graph
    _type = data.get('type', 'tape')

    for _input in inputs:
        value = _input['tape']
        position: PositionInputType|None = _input.get('position')
        tape = _generate_tape(_type, value, position, blank_symbol)

        tapes.append(tape)

    return Machine(configuration, tapes)
