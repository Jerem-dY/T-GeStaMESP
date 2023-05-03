from enum import Enum, Flag, auto


class FuncTypes(Flag):
    
    THROUGH = 0
    ENTRY_POINT = auto()
    END_POINT = auto()