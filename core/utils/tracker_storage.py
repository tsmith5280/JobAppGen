import json

def save_tracker_to_json(tracker_data, filepath):
    with open(filepath, "w") as f:
        json.dump(tracker_data, f, indent=2)

def load_tracker_from_json(file):
    try:
        return json.load(file)
    except Exception as e:
        raise ValueError(f"Invalid JSON tracker: {e}")
