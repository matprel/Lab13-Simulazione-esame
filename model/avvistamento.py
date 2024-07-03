from dataclasses import dataclass
from datetime import date

import datetime


@dataclass
class Avvistamento:
    id: int
    datetime: datetime
    city: str
    state: str
    country: str
    shape: str
    duration: int
    duration_hm: str
    comments: str
    date_posted: date
    latitude: float
    longitude: float