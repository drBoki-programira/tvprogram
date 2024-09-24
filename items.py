from dataclasses import dataclass
from datetime import datetime


@dataclass
class Record:
    time: datetime
    tag: str
    title: str
    descr: str
