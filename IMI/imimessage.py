from json.encoder import ESCAPE
from logging import ERROR
from multiprocessing import Value
from sys import executable
from token import OP
from typing import TypedDict, Dict, Optional, Tuple
from enum import EJECT, Enum, auto

# from networkx import hexagonal_lattice_graph

# TODO:MENUを選んで実行する処理を実行する
# TODO:TOOLにテストモーションを入れたい
# TODO:TOOLにセンサ値を表示させたい
class IMISensorsDict(TypedDict):
    timestamp:int
    wallflag:tuple[Optional[bool], Optional[bool], Optional[bool]]
    wallvalue:tuple[Optional[float], Optional[float], Optional[float]]
    
class RunCmd(Enum):
    STOP        = auto()
    ENDLESS     = auto()
    HALF_STRAGHT = auto()
    STRAIGHT    = auto()
    LEFT_SPINTURN   = auto()
    RIGHT_SPINTURN  = auto()
    LEFT_TURN   = auto()
    RIGHT_TURN  = auto()
    U_TURN      = auto()
    CALIBRATE   = auto()
    CHECK_SNSR = auto()

class JOB_STATE(Enum):
    INIT = 0
    CHOICE = auto()
    EXEC = auto()
    ABORT = auto()
    HALT = auto()

class JOB(Enum):
    ROOT    = auto()
    SEARCH  = auto()
    TOOLS   = auto()
    TEST_MOTIONS = auto()
    TEST_SENSORS = auto()
    TM_STRAIGHT = auto()
    TM_TURN = auto()
    ERROR   = 0

JOB_STR:dict[JOB, str] = {
    JOB.ROOT:                   "ROOT",
    JOB.SEARCH:                 "SRCH",
    JOB.TOOLS:                  "TOLS",
    JOB.TEST_MOTIONS:           "TMOT",
    JOB.TEST_SENSORS:           "TSNS",
    JOB.TM_STRAIGHT:            "TMST",
    JOB.TM_TURN:                "TMTN",
}

class ExecJob:
    Job:JOB
    Argn:int


JOB_ARGN:dict[JOB, int] = {
    JOB.SEARCH: 2,
    JOB.TEST_MOTIONS:   3,
    JOB.TEST_SENSORS:   3,
    JOB.TM_STRAIGHT:    4,
    JOB.TM_TURN:        4,
}

JOB_TABLE:dict[JOB,list[JOB]] = {
#   JOBの名前       キャンセル時の遷移先、以降セレクトの選択肢。セレクトの選択肢が自分自身の場合、実行に入る
    JOB.ERROR:          [   JOB.ERROR,  JOB.ERROR],
    JOB.ROOT:           [   JOB.ROOT,   JOB.SEARCH, JOB.TOOLS],
    JOB.SEARCH:         [   JOB.ROOT,   JOB.SEARCH],
    JOB.TOOLS:          [   JOB.ROOT,   JOB.TEST_MOTIONS, JOB.TEST_SENSORS,],
    JOB.TEST_MOTIONS:   [   JOB.TOOLS,   JOB.TM_STRAIGHT, JOB.TM_TURN],
    JOB.TEST_SENSORS:   [   JOB.TOOLS,   JOB.TEST_SENSORS],
    JOB.TM_STRAIGHT:    [   JOB.TEST_MOTIONS,   JOB.TM_STRAIGHT],
    JOB.TM_TURN:        [   JOB.TEST_MOTIONS,   JOB.TM_TURN],
}


class SoundPattern(Enum):
    NONE_TONE   = 0
    BOOT_0      = auto()
    ABORT_R     = auto()
    ABORT       = auto()
    HALT_R      = auto()
    HALT        = auto()
    EXIT_0      = auto()
    OK_0        = auto()
    OK_1        = auto()
    OK_L        = auto()
    CANCEL_0    = auto()
    CANCEL_1    = auto()
    CANCEL_L    = auto()
    SELECT_0    = auto()
    ERROR_0     = auto()

class MusicalScale(Enum):
    C3 =    int(130.81)    # ド
    CS3 =   int(138.59) 
    D3 =    int(146.83)    # レ
    D3S =   int(155.56)    # レ#
    E3 =    int(164.81)    # ミ
    F3 =    int(174.61)    # ファ
    F3S =   int(185.00)    # ファ#
    G3 =    int(196.00)    # ソ
    G3S =   int(207.65)    # ソ#
    A3 =    int(220.00)    # ラ
    A3S =   int(233.08)    # ラ
    B3 =    int(246.94)    # シ

    C4 =    int(261.63)    # ド
    C4S =   int(277.18)    # ド#
    D4 =    int(293.66)    # レ
    D4S =   int(311.13)    # レ#
    E4 =    int(329.63)    # ミ
    F4 =    int(349.23)    # ファ
    F4S =   int(369.99)    # ファ#
    G4 =    int(392.00)    # ソ
    G4S =   int(415.31)    # ソ#
    A4 =    int(440.00)    # ラ
    A4S =   int(466.16)    # ラ#
    B4 =    int(493.88)    # シ

    C5 =    int(523.25)    # 5ド
    C5S =   int(554.37)    # ドS
    D5 =    int(587.33)    # レ
    D5S =   int(622.25)    # レ#
    E5 =    int(659.25)    # ミ
    F5 =    int(698.46)    # ファ
    F5S =   int(739.99)    # ファS
    G5 =    int(783.99)    # ソ
    G5S =   int(830.61)    # ソS
    A5 =    int(880.00)    # ラ
    A5S =   int(932.33)    # ラS
    B5 =    int(987.77)    # シ

    C6 =    int(1046.50)   # 6 ド
    C6S =   int(1108.73)   # ドS
    D6 =    int(1174.66)   # レ
    D6S =   int(124.51)    # レS
    E6 =    int(1318.51)   # ミ
    F6 =    int(1396.91)   # ファ
    F6S =   int(1479.98)   # ファS
    G6 =    int(1567.98)   # ソ
    G6S =   int(1661.22)   # ソS
    A6 =    int(1760.00)   # ラ
    A6S =   int(1864.66)   # ラS
    B6 =    int(1975.53)   # シ

SoundPatternTABLE:dict[SoundPattern,list[tuple[Optional[int], Optional[float], Optional[float]]]] = {
    SoundPattern.NONE_TONE:     [(None, None, None)],
    # SoundPattern.BOOT_0:        [   (MusicalScale.F5S.value,    0.2, None),    # ファ#5
    #                                 (MusicalScale.D5.value,     0.2, None),     # レ5
    #                                 (MusicalScale.A4.value,     0.2, None),     # ラ4
    #                                 (MusicalScale.D5.value,     0.2, 0.01),     # レ5
    #                                 (MusicalScale.E5.value,     0.2, None),     # ミ5
    #                                 (MusicalScale.A5.value,     0.2, 0.2),      # ラ5
    #                                 (MusicalScale.E4.value,     0.2, 0.01),     # ミ4
    #                                 (MusicalScale.F5.value,     0.2, None),     # ミ5
    #                                 (MusicalScale.F5S.value,    0.2, None),    # ファ#5
    #                                 (MusicalScale.F5.value,     0.2, None),     # ミ5
    #                                 (MusicalScale.A4.value,     0.2, 0.01),     # ラ4
    #                                 (MusicalScale.D5.value,     0.3, 0.01),     # レ5
    #                             ],
    SoundPattern.BOOT_0:        [
                                    (MusicalScale.C3.value,     0.1, None),
                                    (MusicalScale.C4.value,     0.1, None),
                                    (MusicalScale.C5.value,     0.1, None),
                                    (MusicalScale.C6.value,     0.1, None),
                                    (MusicalScale.B6.value,     0.5, 0),
    ],
    SoundPattern.ABORT_R:       [   
                                    (MusicalScale.C5S.value,    0.5, None),
                                    (MusicalScale.B3.value,     0.25, None),
    ],
    SoundPattern.ABORT:         [   
                                    (MusicalScale.C5S.value,    0.5, None),
                                    (MusicalScale.B3.value,     0.25, None),
                                    (MusicalScale.C5S.value,    0.5, None),
                                    (MusicalScale.B3.value,     0.25, None),
                                    (MusicalScale.C5S.value,    0.5, None),
                                    (MusicalScale.B3.value,     0.25, 0),
    ],

    SoundPattern.EXIT_0:        [   
                                    (MusicalScale.B5.value,     0.1, None),
                                    (MusicalScale.C4S.value,    0.2, None),
                                    (MusicalScale.F3S.value,    0.2, None),
                                    (MusicalScale.C3.value,     0.5, 0),
    ],

    SoundPattern.HALT_R:        [   
                                    (MusicalScale.G5S.value,    0.2, None),
                                    (MusicalScale.B4.value,     0.1, None),
    ],

    SoundPattern.HALT:          [   
                                    (MusicalScale.G5S.value,    0.5, None),
                                    (MusicalScale.B4.value,     0.25, None),
                                    (MusicalScale.E4.value,    0.5, None),
                                    (MusicalScale.F4S.value,     0.25, None),
                                    (MusicalScale.G5S.value,    0.5, None),
                                    (MusicalScale.F4S.value,     0.25, 0),
    ],

    SoundPattern.OK_0:          [
                                    (MusicalScale.E5.value,    0.25, 0),
    ],
    
    SoundPattern.OK_1:          [
                                    (MusicalScale.G5.value,    0.1, 0.1),
                                    (MusicalScale.G5.value,    0.1, 0),
    ],

    SoundPattern.OK_L:          [
                                    (MusicalScale.E5.value,    0.2, None),
    ],

    SoundPattern.CANCEL_0:      [
                                    (MusicalScale.F4S.value,    0.1, 0.1),
                                    (MusicalScale.C4S.value,    0.1, 0),
    ],
    SoundPattern.CANCEL_1:      [
                                    (MusicalScale.F4S.value,    0.1, 0.1),
                                    (MusicalScale.C4S.value,    0.1, 0.1),
                                    (MusicalScale.F4S.value,    0.1, 0.1),
                                    (MusicalScale.C4S.value,    0.1, 0),
    ],
    SoundPattern.CANCEL_L:      [
                                    (MusicalScale.F4S.value,    0.1, 0.1),
                                    (MusicalScale.C4S.value,    0.1, None),
    ],

    SoundPattern.SELECT_0:      [
                                    (MusicalScale.F6S.value,    0.1, 0),
    ],
    SoundPattern.ERROR_0  :     [
                                    (MusicalScale.F3S.value,    0.2, 0.1),
                                    (MusicalScale.F3S.value,    0.2, 0),
    ],
}

