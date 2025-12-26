# logic.py
from datetime import datetime

def berechne_monatsschulden(schulden, monat, jahr):
    return sum(
        float(s["betrag"])
        for s in schulden
        if datetime.strptime(s["datum"], "%Y-%m-%d %H:%M").month == monat
        and datetime.strptime(s["datum"], "%Y-%m-%d %H:%M").year == jahr
    )


def berechne_jahresschulden(schulden, jahr):
    return sum(
        float(s["betrag"])
        for s in schulden
        if datetime.strptime(s["datum"], "%Y-%m-%d %H:%M").year == jahr
    )
