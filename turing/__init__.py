"""Simulates a turing machine, with a simple tape or a '2d tape'"""

import json
from typing import List, Optional, Union

import numpy as np

from .errors import (JSONDecodeError, UnexpectedDirection, UnexpectedState,
                     UnexpectedType)
from .types import (DirectionType, InstructionInputType,
                    MachineConfigurationType, Position2dInputType,
                    Position2dType, PositionTapeInputType, StatesInputType,
                    StateType, SymbolType, TapeType2dType, TapeTypeTapeType)


def generate_machine_from_dict(data: MachineConfigurationType):
    """Generate a turing machine by dict"""

    start_state = data['start-state']
    else_sign = data.get('else-sign', None)
    states = data['states']

    configuration = MachineConfiguration(states, start_state, else_sign)

    blank_symbol = data.get('blank-symbol', ' ')

    _type = data.get('type', 'tape')

    inputs = data['inputs']

    if _type == 'tape':
        tapes = [
            Tape(_input['tape'], _input.get('position'), blank_symbol)
            for _input in inputs
        ]
    elif _type == '2d':
        tapes = [
            Tape2d(_input['tape'], _input.get('position'), blank_symbol)
            for _input in inputs
        ]
    else:
        raise UnexpectedType("Unexpected type of machine")

    return Machine(configuration, tapes)

class Instruction:
    """The Instruction of turing machine"""

    def __init__(self, data: Optional[InstructionInputType] = None):
        self.direction: Optional[DirectionType] = None
        self.new_state: Optional[StateType] = None
        self.write = None
        if data is not None:
            if isinstance(data, str):
                self.direction = data
            elif len(data) == 1:
                self.direction = data[0]
            elif len(data) == 2:
                self.direction = data[0]
                self.new_state = data[1]
            elif len(data) == 3:
                self.direction = data[0]
                self.new_state = data[1]
                self.write     = data[2]
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

    type = 'tape'

    DIRECTIONS = {
        'R': +1,
        'L': -1
    }

    def __init__(self, tape: TapeTypeTapeType, position: Optional[PositionTapeInputType] = None,
                 blank_symbol: SymbolType = ' ') -> None:
        if position is None:
            position = 0

        self.position = int(position)
        self.tape = dict(zip(range(len(tape)), tape))
        self.blank_symbol = blank_symbol

    def __str__(self) -> str:
        min_position = min(self.tape)
        max_position = max(self.tape)

        return ''.join(self[pos]
                       for pos in range(min_position, max_position+1))

    def __repr__(self) -> str:
        cls = self.__class__

        min_position = min(self.tape)
        tape = str(self)

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

    def __setitem__(self, position: int, value: str):
        if value == self.blank_symbol:
            del self.tape[position]
        else:
            self.tape[position] = value

    def read_pointer(self) -> str:
        """Read the tape head char"""

        return self[self.position]

    def do_instruction(self, instruction: Instruction):
        """Execute an instruction of turing machine"""

        if instruction.write is not None:
            self[self.position] = instruction.write

        if instruction.direction not in self.DIRECTIONS:
            raise UnexpectedDirection(f"Unexpected direction: \"{instruction.direction}\"")

        self.position += self.DIRECTIONS[instruction.direction]


class Tape2d:
    """The tape of turing machine"""

    type = '2d'

    DIRECTIONS = {
        'R': np.array((1,  0), np.int_),
        'L': np.array((-1, 0), np.int_),
        'D': np.array((0,  1), np.int_),
        'U': np.array((0, -1), np.int_)
    }

    def __init__(self, tape: TapeType2dType, position: Optional[Position2dInputType] = None,
                 blank_symbol: SymbolType = ' ') -> None:

        self.tape = {}
        if position is None:
            self.position = np.zeros((2), np.int_)
        else:
            self.position = np.array(position)
        self.blank_symbol = blank_symbol

        for i, line in enumerate(tape):
            for j, cell in enumerate(line):
                self[np.array((j, i), np.int_)] = cell

    def __repr__(self) -> str:
        cls = self.__class__

        content = [repr(self.tape)]
        if (self.position != 0).any():
            content.append(str(self.position))
        if self.blank_symbol != ' ':
            content.append(f"blank_symbol={self.blank_symbol}")

        return f"{cls.__name__}({', '.join(content)})"

    def __getitem__(self, position: Position2dType):
        str_position = f"{position[0]} {position[1]}"

        if str_position in self.tape:
            return self.tape[str_position]

        return self.blank_symbol

    def __setitem__(self, position: Position2dType, value):
        str_position = f"{position[0]} {position[1]}"

        if value == self.blank_symbol:
            if str_position in self.tape:
                del self.tape[str_position]
        else:
            self.tape[str_position] = value

    def __str__(self):
        all_cords = tuple(cord.split(' ') for cord in self.tape)
        x_cords = [int(cord[0]) for cord in all_cords]

        y_cords = [int(cord[1]) for cord in all_cords]
        y_cords = np.arange(min(y_cords, default=0), max(y_cords, default=0)+1, 1)

        str_tape = ''
        for y in y_cords:
            for i in range(min(x_cords, default=0), max(x_cords, default=0)+1):
                str_tape += self[np.array((i, y), np.int_)]
            str_tape += '\n'

        return str_tape

    def read_pointer(self) -> str:
        """Read the tape head char"""

        return self[self.position]

    def do_instruction(self, instruction: Instruction):
        """Execute an instruction of turing machine"""

        if instruction.write is not None:
            self[self.position] = instruction.write

        if instruction.direction not in self.DIRECTIONS:
            raise UnexpectedDirection(f"Unexpected direction: \"{instruction.direction}\"")

        self.position += self.DIRECTIONS[instruction.direction]


class MachineConfiguration:
    """Configuration of turing machine"""

    def __init__(self, states: StatesInputType, start_state: StateType,
                 else_sign: Optional[SymbolType] = None) -> None:
        if start_state not in states:
            raise UnexpectedState(
                f"Expected state \"{start_state}\" in states, but no found")

        self.states = states
        self.start_state = start_state
        self.else_sign = else_sign

    def __repr__(self) -> str:
        cls = self.__class__
        return f"{cls.__name__}(dict(...), {self.start_state!r}, {self.else_sign!r})"

    def get_instruction(self, state: StateType, char: str) -> Instruction:
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

    def __init__(self, configuration: MachineConfiguration,
                 tapes: Union[List[Tape], List[Tape2d]]) -> None:
        self.configuration = configuration
        self.tapes = tapes
        self.state: str = configuration.start_state

    def __repr__(self) -> str:
        cls = self.__class__
        return f"{cls.__name__}({self.configuration!r}, {self.tapes!r})"

    def step(self, tape: Union[Tape, Tape2d]):
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
