# ============================================
# Django Standalone Subject Seeder
# Run using: python generator/scripts/seed_subjects.py
# ============================================

import os
import sys
import django
from pathlib import Path

# 🔥 Load project root (2 levels up from scripts/)
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SyncSchedule.settings")
django.setup()

from generator.models import Subject


subjects = [
    # Semester 1
    {"name": "Maths", "sem": 1, "lec": 4, "lab": 0},
    {"name": "ENG", "sem": 1, "lec": 2, "lab": 0},

    # Semester 2
    {"name": "DM", "sem": 2, "lec": 3, "lab": 0},
    {"name": "JT", "sem": 2, "lec": 3, "lab": 0},
    {"name": "MTS", "sem": 2, "lec": 2, "lab": 2},

    # Semester 3
    {"name": "PPS II", "sem": 3, "lec": 3, "lab": 2},
    {"name": "DDC", "sem": 3, "lec": 3, "lab": 0},
    {"name": "CSA", "sem": 3, "lec": 3, "lab": 0},
    {"name": "HW1", "sem": 3, "lec": 0, "lab": 2},
    {"name": "HW2", "sem": 3, "lec": 0, "lab": 2},

    # Semester 4
    {"name": "DAA", "sem": 4, "lec": 4, "lab": 0},
    {"name": "SEPP", "sem": 4, "lec": 3, "lab": 0},
    {"name": "ACA", "sem": 4, "lec": 3, "lab": 2},

    # Semester 5
    {"name": "CN", "sem": 5, "lec": 4, "lab": 0},
    {"name": "ML", "sem": 5, "lec": 3, "lab": 2},
    {"name": "WSD", "sem": 5, "lec": 2, "lab": 2},

    # Semester 6
    {"name": "TAFL", "sem": 6, "lec": 3, "lab": 0},
    {"name": "BDA", "sem": 6, "lec": 3, "lab": 2},
    {"name": "SC", "sem": 6, "lec": 2, "lab": 2},
    {"name": "SP", "sem": 6, "lec": 2, "lab": 2},
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

print("\n====================================")
print(f"✅ Subjects inserted successfully! ({created_count} new)")
print("====================================")