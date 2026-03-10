import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SyncSchedule.settings")
django.setup()

from generator.models import RoomLab

rooms = [
    # Classrooms
    {"roomNo": "R3", "type": "CLASSROOM"},
    {"roomNo": "R4", "type": "CLASSROOM"},
    {"roomNo": "R5", "type": "CLASSROOM"},
    {"roomNo": "R6", "type": "CLASSROOM"},
    {"roomNo": "R30", "type": "CLASSROOM"},
    {"roomNo": "R31", "type": "CLASSROOM"},

    # Labs
    {"roomNo": "L1", "type": "LAB"},
    {"roomNo": "L2", "type": "LAB"},
    {"roomNo": "L3", "type": "LAB"},
    {"roomNo": "L4", "type": "LAB"},
    {"roomNo": "L5", "type": "LAB"},
    {"roomNo": "L6", "type": "LAB"},
    {"roomNo": "L7", "type": "LAB"},
    {"roomNo": "L8", "type": "LAB"},

    # Seminar Hall
    {"roomNo": "Seminar Hall", "type": "SEMINAR HALL"},
]

def get_capacity(room_type):
    if room_type == "CLASSROOM":
        return 90
    elif room_type == "LAB":
        return 40
    elif room_type == "SEMINAR HALL":
        return 100
    return 50  # fallback

for r in rooms:
    RoomLab.objects.get_or_create(
        roomNo=r["roomNo"],
        defaults={
            "room_type": r["type"],
            "capacity": get_capacity(r["type"]),
            "isAvailable": True
        }
    )

print("Rooms, labs and capacities inserted successfully!")
