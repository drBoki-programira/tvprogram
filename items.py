from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


@dataclass
class Record:
    time: datetime
    tag: str
    title: str
    descr: str


class Days(timedelta, Enum):
    DANAS = 0
    SUTRA = 1
    PREKOSUTRA = 2
    NAKOSUTRA = 3
