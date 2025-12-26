# database.py
import json
import os
from models import SchuldEintrag, BezahlterEintrag

SCHULDNER_FILE = "schuldner.json"
SCHULDGEBER_FILE = "schuldgeber.json"
BEZAHLT_FILE = "bezahlt.json"


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ------------------ SCHULDEN ------------------

def load_schulden():
    return load_json(SCHULDNER_FILE)


def save_schulden(data):
    save_json(SCHULDNER_FILE, data)


def add_schuld(eintrag: SchuldEintrag):
    data = load_schulden()
    data.append(eintrag.__dict__)
    save_schulden(data)


def delete_schuld(index):
    data = load_schulden()
    if 0 <= index < len(data):
        data.remove(data[index])
        save_schulden(data)


# ------------------ BEZAHLTE SCHULDEN ------------------

def load_bezahlt():
    return load_json(BEZAHLT_FILE)


def save_bezahlt(data):
    save_json(BEZAHLT_FILE, data)


def add_bezahlt(eintrag: BezahlterEintrag):
    data = load_bezahlt()
    data.append(eintrag.__dict__)
    save_bezahlt(data)
