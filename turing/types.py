"""Types of this turing machine"""

from typing import List, Literal, Optional, Tuple, TypeAlias, TypedDict, Union

import numpy as np
import numpy.typing as npt

StateType: TypeAlias = str
SymbolType: TypeAlias = str
DirectionType = Union[Literal["R"], Literal["L"], Literal["D"], Literal["U"]]
SymbolsType: TypeAlias = str

PositionTapeInputType: TypeAlias = int
Position2dInputType = List[int]
PositionInputType = Union[PositionTapeInputType, Position2dInputType]

PositionTapeType = int
Position2dType = npt.NDArray[np.int_]
PositionType = Union[Position2dType, PositionTapeType]

TapeTypeTapeType = SymbolsType
TapeType2dType = List[SymbolsType]

class InputTapeType(TypedDict):
    """Dict input type"""
    tape: TapeTypeTapeType
    position: PositionTapeInputType

class Input2dType(TypedDict):
    """Dict input type"""
    tape: TapeType2dType
    position: Position2dInputType

InstructionInputType = Union[DirectionType, Tuple[DirectionType, StateType, SymbolType]]
StatesInputType = dict[StateType, dict[SymbolsType, InstructionInputType]]
InputsType = List[Union[InputTapeType, Input2dType]]

MachineTypeTapeConfigurationType = TypedDict('MachineConfigurationType', {
    'type': Optional[Literal['tape']],
    'states': StatesInputType,
    'start-state': StateType,
    'inputs': List[InputTapeType],
    'blank-symbol': SymbolType,
    'else-sign': SymbolType
})

MachineType2dConfigurationType = TypedDict('MachineConfigurationType', {
    'type': Literal['2d'],
    'states': StatesInputType,
    'start-state': StateType,
    'inputs': List[Input2dType],
    'blank-symbol': SymbolType,
    'else-sign': SymbolType
})

MachineConfigurationType = Union[MachineTypeTapeConfigurationType, MachineType2dConfigurationType]
