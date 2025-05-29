import json
from datetime import datetime, timedelta,timezone

def load_messages(path="texts.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


messages = load_messages()
print(messages["checklist"].format(hour=datetime.now().hour, minute=datetime.now().minute))
# print(messages["ch"])