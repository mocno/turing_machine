import json
from typing import Union

class TuringMachine:
    def __init__(self, start_state: str, all_symbols: list[str], states: dict[str, dict[str, list[str]]], else_sign: Union[str, None]=None):
        self.current_state = self.start_state = start_state
        self.all_symbols = all_symbols
        self.states = states
        self.else_sign = else_sign

    def step(self, value):
        instruction = self.states.get(self.current_state, None)

        if instruction is None:
            return None

        if value in instruction:
            return instruction[value]

        for key, values in instruction.items():
            if value in key:
                return values

        if self.else_sign is None:
            return None

        return instruction.get(self.else_sign, None)

    def set_state(self, new_state):
        self.current_state = new_state

class Tape:
    def __init__(self, tape: str, black_symbol: str=' ', position: int=0):
        self.tape = dict(zip(range(len(tape)), tape))
        self.black_symbol = black_symbol
        self.position = position

    def __getitem__(self, position: int):
        if position in self.tape:
            return self.tape[position]

        return self.black_symbol

    def __setitem__(self, position, value):
        self.tape[position] = value

    def __str__(self):
        return ''.join(self[position] for position in range(min(self.tape.keys()) - 2, max(self.tape.keys()) +3)) + '\n' + (self.position - min(self.tape.keys()) + 2) * ' ' + '^'

    def run(self, turing_machine_config: TuringMachine):
        steps = 0
        while True:
            steps += 1
            instruction = turing_machine_config.step(self[self.position])

            print(turing_machine_config.current_state)
            print(self)

            if instruction is None:
                print("steps:", steps)
                return True

            if len(instruction) == 1:
                _dir, *_ = instruction
            elif len(instruction) == 2:
                _dir, new_state, *_ = instruction
                turing_machine_config.set_state(new_state)
            elif len(instruction) == 3:
                _dir, new_state, write = instruction
                self[self.position] = write
                turing_machine_config.set_state(new_state)
            else:
                return False

            if _dir == "L":
                self.position -= 1
            elif _dir == "R":
                self.position += 1


def read_json_machine_config(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.read()

    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError:
        return None, None

    turing_machine_config = TuringMachine(
        data['start-state'],
        data['all-symbols'],
        data['states'],
        data['else-sign']
    )

    tapes: list[Tape] = []
    for _input in data["inputs"]:
        position = 0
        if "position" in _input:
            position = _input["position"]

        tape = Tape(_input["tape"], data['black-symbol'], position)

        tapes.append(tape)

    return turing_machine_config, tapes
