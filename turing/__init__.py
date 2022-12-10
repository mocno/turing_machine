"""Simulates a turing machine, with a simple tape or a '2d tape'"""

from typing import Union, List
import json
from .errors import JSONDecodeError, UnexpectedState, TapeIndexError, UnexpectedDirection


def generate_machine_from_dict(data):
    """Generate a turing machine by dict"""

    states = data['states']
    start_state = data['start-state']
    else_sign = data.get('else-sign', None)

    configuration = MachineConfiguration(states, start_state, else_sign)

    blank_symbol = data.get('blank-symbol', ' ')

    tapes = []

    try:
        inputs: list = data['inputs']
    except KeyError:
        return Machine(configuration, tapes)

    tapes = []

    for _input in inputs:
        tape = _input['tape']
        position = _input.get('position', 0)
        tape = Tape(tape, position, blank_symbol)

        tapes.append(tape)

    # _type = data.get('type', 'tape') // tape 2d graph(???)

    return Machine(configuration, tapes)


class Instruction:
    """The Instruction of turing machine"""

    def __init__(self, data: Union[str, list, None] = None):
        self.direction = None
        self.new_state = None
        self.write = None
        if data is not None:
            if isinstance(data, str):
                data = data.split(' ')

            if len(data) == 1:
                self.direction, *_ = data
            elif len(data) == 2:
                self.direction, self.new_state = data
            elif len(data) == 3:
                self.direction, self.new_state, self.write = data
            else:
                raise ValueError("Not expected instruction")

    def __repr__(self) -> str:
        cls = self.__class__

        if self.direction is None:
            return f"{cls.__name__}()"

        contents = ' '.join(
            str(content)
            for content in (self.direction, self.new_state, self.write)
            if content is not None
        )

        return f"{cls.__name__}({contents!r})"

    def stopped(self) -> bool:
        """Return if instruction is to stop the machine"""
        return self.direction is None and self.new_state is None and self.write is None


class Tape:
    """The tape of turing machine"""

    DIRECTIONS = {
        'R': +1,
        'L': -1
    }

    def __init__(self, tape: str, position: int = 0, blank_symbol: str = ' ') -> None:
        self.tape = dict(zip(range(len(tape)), tape))
        self.position = position
        self.blank_symbol = blank_symbol

    def __repr__(self) -> str:
        cls = self.__class__

        min_position = min(self.tape)
        max_position = max(self.tape)

        tape = ''.join(self[pos]
                       for pos in range(min_position, max_position+1))

        content = [repr(tape)]
        if self.position != min_position:
            content.append(str(self.position-min_position))
        if self.blank_symbol != ' ':
            content.append(f"blank_symbol={self.blank_symbol}")

        return f"{cls.__name__}(" + ', '.join(content) + ")"

    def __getitem__(self, position: int):
        if position in self.tape:
            return self.tape[position]

        return self.blank_symbol

    def __setitem__(self, position, value):
        if value == self.blank_symbol:
            del self.tape[position]
        else:
            self.tape[position] = value

    def read_pointer(self) -> str:
        """Read the tape head char"""

        return self[self.position]

    def set_pointer(self, value):
        """Set the tape head char"""

        self[self.position] = value

    def do_instruction(self, instruction):
        """Execute an instruction of turing machine"""

        if instruction.write is not None:
            self.set_pointer(instruction.write)

        if instruction.direction not in self.DIRECTIONS:
            raise UnexpectedDirection(f"Unexpected direction: \"{instruction.direction}\"")

        self.position += self.DIRECTIONS[instruction.direction]


class MachineConfiguration:
    """Configuration of turing machine"""

    def __init__(self, states: dict[str, dict[str, Union[str, list]]],
            start_state: str, else_sign: Union[str, None] = None) -> None:
        if start_state not in states:
            raise UnexpectedState(
                f"Expected state \"{start_state}\" in states, but no found")

        self.states = states
        self.start_state = start_state
        self.else_sign = else_sign

    def __repr__(self) -> str:
        cls = self.__class__
        return f"{cls.__name__}(dict(...), {self.start_state!r}, {self.else_sign!r})"

    def get_instruction(self, state: str, char: str) -> Instruction:
        """Get instruction of configuration by state and tape head char"""

        if state not in self.states:
            raise UnexpectedState(f"Unexpected state \"{state}\", not found")

        instructions_by_state = self.states[state]

        if char in instructions_by_state:
            return Instruction(instructions_by_state[char])

        for chars, instruction in instructions_by_state.items():
            if char in chars:
                return Instruction(instruction)

        if self.else_sign in instructions_by_state:
            return Instruction(instructions_by_state[self.else_sign])

        return Instruction()


class Machine:
    """Instance of turing machine"""

    def __init__(self, configuration: MachineConfiguration, tapes: List[Tape]) -> None:
        self.configuration = configuration
        self.tapes = tapes
        self.state = configuration.start_state

    def __repr__(self) -> str:
        cls = self.__class__
        return f"{cls.__name__}({self.configuration!r}, {self.tapes!r})"

    def run(self, index: int):
        """Start the machine"""

        try:
            tape = self.tapes[index]
        except IndexError as exception:
            raise TapeIndexError("The index out of range") from exception

        while True:
            _continue = self.step(tape)

            if not _continue:
                break

    def step(self, tape):
        """Do a machine step"""

        char = tape.read_pointer()

        instruction = self.configuration.get_instruction(self.state, char)

        if instruction.stopped():
            return False

        if instruction.new_state is not None:
            self.state = instruction.new_state

        tape.do_instruction(instruction)

        return True


def parse_json_machine(filepath: str, encoding: str = "utf-8") -> Machine:
    """Parse from a json file configurations of a turing machine"""

    with open(filepath, 'r', encoding=encoding) as file:
        data = file.read()

    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError as exception:
        raise JSONDecodeError("The file has some json error") from exception

    return generate_machine_from_dict(data)
