import os
import sys
import django
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SyncSchedule.settings")
django.setup()

from generator.models import Subject


subjects = [

    # Semester 1
    {"name": "Maths-I", "sem": 1, "lec": 3, "lab": 0},
    {"name": "EGD", "sem": 1, "lec": 1, "lab": 2},
    {"name": "PPS-I", "sem": 1, "lec": 4, "lab": 2},
    {"name": "SWS", "sem": 1, "lec": 0, "lab": 2},
    {"name": "YW", "sem": 1, "lec": 2, "lab": 2},
    {"name": "BEE", "sem": 1, "lec": 4, "lab": 2},



    # Semester 2
    {"name": "ENG", "sem": 2, "lec": 3, "lab": 2},
    {"name": "ES", "sem": 2, "lec": 3, "lab": 0},
    {"name": "HW2", "sem": 2, "lec": 0, "lab": 2},
    {"name": "HW1", "sem": 2, "lec": 0, "lab": 2},
    {"name": "PPS-II", "sem": 2, "lec": 4, "lab": 2},
    {"name": "MATHS-II", "sem": 2, "lec": 3, "lab": 0},


    # Semester 3
    {"name": "DDC", "sem": 3, "lec": 3, "lab": 2},
    {"name": "UHV", "sem": 3, "lec": 3, "lab": 0},
    {"name": "DSA", "sem": 3, "lec": 4, "lab": 2},
    {"name": "DBMS", "sem": 3, "lec": 4, "lab": 2},
    {"name": "WDW", "sem": 3, "lec": 0, "lab": 2},
    {"name": "EIKT", "sem": 3, "lec": 3, "lab": 0},

    # Semester 4
    {"name": "CSA", "sem": 4, "lec": 3, "lab": 2},
    {"name": "JT", "sem": 4, "lec": 4, "lab": 2},
    {"name": "DM", "sem": 4, "lec": 3, "lab": 0},
    {"name": "DAA", "sem": 4, "lec": 4, "lab": 2},
    {"name": "SEPP", "sem": 4, "lec": 2, "lab": 2},
    {"name": "SP", "sem": 4, "lec": 0, "lab": 2},

    # Semester 5
    {"name": "AA", "sem": 5, "lec": 4, "lab": 2},
    {"name": "OS", "sem": 5, "lec": 4, "lab": 2},
    {"name": "AT", "sem": 5, "lec": 3, "lab": 2},
    {"name": "MFP", "sem": 5, "lec": 2, "lab": 2},
    {"name": "WAD", "sem": 5, "lec": 3, "lab": 2},

    # Semester 6
    {"name": "WSD", "sem": 6, "lec": 3, "lab": 2},
    {"name": "ML", "sem": 6, "lec": 4, "lab": 2},
    {"name": "CN", "sem": 6, "lec": 4, "lab": 2},
    {"name": "ACA", "sem": 6, "lec": 2, "lab": 2},
    {"name": "TAFL", "sem": 6, "lec": 3, "lab": 0},
    {"name": "SDP", "sem": 6, "lec": 0, "lab": 2},


    # Semester 7
    {"name": "CLC", "sem": 7, "lec": 3, "lab": 2},
    {"name": "COC", "sem": 7, "lec": 3, "lab": 0},
    {"name": "BDA", "sem": 7, "lec": 2, "lab": 2},
    {"name": "AI", "sem": 7, "lec": 4, "lab": 0},
    {"name": "CCIT", "sem": 7, "lec": 2, "lab": 2},
    {"name": "DL", "sem": 7, "lec": 4, "lab": 0},
]

created_count = 0

for s in subjects:
    obj, created = Subject.objects.get_or_create(
        subject_name=s["name"],
        defaults={
            "subject_code": s["name"].replace(" ", "_").upper(),
            "semester": s["sem"],
            "lecture_hours": s["lec"],
            "lab_hours": s["lab"]
        }
    )

    if created:
        created_count += 1
        print(f"✔ Created: {s['name']}")
    else:
        print(f"• Already exists: {s['name']}")

print(f"Subjects inserted successfully! ({created_count} new)")
