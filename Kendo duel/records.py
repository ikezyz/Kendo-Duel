import json
import os
from datetime import datetime


RECORDS_FILE = "battle_records.json"
RECORDS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), RECORDS_FILE)


def load_records():
    """Load battle records safely and create the JSON file if it is missing."""
    if not os.path.exists(RECORDS_PATH):
        save_records([])
        return []

    try:
        with open(RECORDS_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            print("Record file format was invalid. Starting with empty records.")
            save_records([])
            return []
    except (json.JSONDecodeError, OSError):
        print("Battle records could not be loaded. Starting with empty records.")
        save_records([])
        return []


def save_records(records):
    """Save all battle records to the JSON file."""
    try:
        with open(RECORDS_PATH, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
    except OSError:
        print("Warning: Battle records could not be saved.")


def add_record(record):
    """Add one completed game record to battle_records.json."""
    records = load_records()
    record_with_time = {
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "result": record["result"],
        "stage_reached": record["stage_reached"],
        "defeated_bots": record["defeated_bots"],
        "final_player_hp": record["final_player_hp"],
    }
    records.append(record_with_time)
    save_records(records)


def reset_records():
    """Clear all saved battle records."""
    save_records([])
