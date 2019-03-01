from enum import Enum


class CmdType(Enum):
    VERIFY = "VER"
    TMP = "TMP"
    ADD_RECORD = "ADR"
    REGISTER = "REG"
    LOGIN = "LOG"
    END = "END"
