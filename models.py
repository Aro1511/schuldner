# models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SchuldEintrag:
    schuldner: str
    schuldgeber: str
    art: str
    betrag: float
    datum: str = datetime.now().strftime("%Y-%m-%d %H:%M")

@dataclass
class BezahlterEintrag:
    schuldner: str
    betrag: float
    datum: str = datetime.now().strftime("%Y-%m-%d %H:%M")
