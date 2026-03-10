from pathlib import Path
import sys
import os
import django

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SyncSchedule.settings")
django.setup()

from django.contrib.auth import get_user_model
from generator.models import FacultyProfile, Subject

User = get_user_model()

def create_faculty(username, email, department, subjects_list, workload):
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "role": "FACULTY"}
    )

    user.set_password("faculty123")
    user.save()

    profile, _ = FacultyProfile.objects.get_or_create(user=user)
    profile.department = department
    profile.workload_hours = workload
    profile.save()

    subjects = Subject.objects.filter(subject_name__in=subjects_list)
    profile.subjects.set(subjects)

    print(f"Created: {username}")


faculty_data = [
    ("JHB", "jhb@ddu.ac.in", "CE", ["DDC","SP","ES"], 16),
    ("CRC", "crc@ddu.ac.in", "CE", ["PPS-I","PPS-II","TAFL"], 14),
    ("KMP", "kmp@ddu.ac.in", "CE", ["Maths-I","MATHS-II","BEE"], 12),
    ("VBP", "vbp@ddu.ac.in", "CE", ["Maths-I","MATHS-II"], 12),
    ("JP", "jp@ddu.ac.in", "CE", ["DAA","EGD","ENG"], 16),
    ("MTM", "mtm@ddu.ac.in", "CE", ["EIKT","SEPP"], 16),
    ("AKG", "akg@ddu.ac.in", "CE", ["DAA","DSA","AA","ACA"], 14),
    ("NJB", "njb@ddu.ac.in", "CE", ["HW1","JT"], 14),
    ("VS", "vs@ddu.ac.in", "CE", ["JT","WAD","HW2"], 14),
    ("AMS", "ams@ddu.ac.in", "CE", ["SEPP","UHV","DM"], 12),
    ("SDP", "sdp@ddu.ac.in", "CE", ["SEPP","OS","AT"], 12),
    ("PS", "ps@ddu.ac.in", "CE", ["CSA","CN","COC"], 14),
    ("SBB", "sbb@ddu.ac.in", "CE", ["SWS","CSA","AT"], 14),
    ("NF", "nf@ddu.ac.in", "CE", ["ACA","MFP","CSA"], 12),
    ("AAM", "aam@ddu.ac.in", "CE", ["ML","TAFL","DM","DSA"], 16),
    ("VVI", "vvi@ddu.ac.in", "CE", ["ML","DL","DSA"], 16),
    ("SPM", "spm@ddu.ac.in", "CE", ["CN","MFP"], 14),
    ("BMG", "bmg@ddu.ac.in", "CE", ["CN","DDC"], 14),
    ("APV", "apv@ddu.ac.in", "CE", ["WSD","WAD","DBMS","OS","YW"], 12),
    ("CKB", "ckb@ddu.ac.in", "CE", ["TAFL","AI","CLC"], 12),
    ("BSB", "bsb@ddu.ac.in", "CE", ["SDP","CCIT","BDA"], 10),
    ("HAP", "hap@ddu.ac.in", "CE", ["SP","CLC","WDW"], 10),
    ("JMP", "jmp@ddu.ac.in", "CE", ["SP","DL","BDA"], 10),
]

for f in faculty_data:
    create_faculty(*f)

print("Faculty seeding complete!")
