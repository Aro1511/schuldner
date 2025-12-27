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


# ---------------------------------------------------------
# NEUE FUNKTION: Betrag berechnen aus Text (z.B. "2,00 + 1,99")
# ---------------------------------------------------------

def berechne_betrag(eingabe: str):
    """Berechnet einen Betrag aus einer Texteingabe wie '2,00 + 1,99'."""
    if not eingabe:
        return None

    # Komma zu Punkt
    eingabe = eingabe.replace(",", ".")

    # Nur sichere Zeichen erlauben
    erlaubte_zeichen = "0123456789.+-*/() "
    if any(c not in erlaubte_zeichen for c in eingabe):
        return None

    try:
        # eval ist hier sicher, weil wir die Zeichen vorher filtern
        return round(eval(eingabe), 2)
    except:
        return None
