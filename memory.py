import json
import os

NOTES_FILE = "notes.json"


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []

    with open(NOTES_FILE, "r") as f:
        return json.load(f)


def save_note(note):
    notes = load_notes()

    notes.append(note)

    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)


def get_notes():
    notes = load_notes()

    if not notes:
        return "No saved notes."

    return "\n".join(notes)