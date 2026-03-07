import os
import sys
import django
import random
from collections import defaultdict

print("Initializing timetable generation...")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SyncSchedule.settings")
django.setup()

from generator.models import (
    TimeSlot,
    Subject,
    FacultyProfile,
    RoomLab,
    TimetableEntry,
)


def generate_all_timetables():

    print("Generating full timetable...")

    TimetableEntry.objects.all().delete()

    semesters = [1,2,3,4,5,6,7]
    divisions = ["A1","A2","A3","A4","B1","B2","B3","B4"]

    lecture_rooms = list(RoomLab.objects.filter(room_type="CLASSROOM", isAvailable=True))
    lab_rooms = list(RoomLab.objects.filter(room_type="LAB", isAvailable=True))

    slots = list(TimeSlot.objects.filter(is_break=False).order_by("day","start_time"))

    # ---------------- FACULTY MAP ----------------

    faculty_map = defaultdict(list)

    for f in FacultyProfile.objects.all():
        for s in f.subjects.all():
            faculty_map[s.id].append(f)

    # ---------------- BUSY TRACKERS ----------------

    faculty_busy = defaultdict(set)
    room_busy = defaultdict(set)
    division_busy = defaultdict(set)
    lab_day_used = defaultdict(set)

    created = 0

    # =================================================
    # LAB SCHEDULING
    # =================================================

    for semester in semesters:
        for division in divisions:

            subjects = list(Subject.objects.filter(semester=semester))
            random.shuffle(subjects)

            for subject in subjects:

                if subject.lab_hours <= 0:
                    continue

                faculties = faculty_map.get(subject.id, [])

                for i in range(len(slots)-1):

                    if subject.lab_hours <= 0:
                        break

                    slot1 = slots[i]
                    slot2 = slots[i+1]

                    if slot1.day != slot2.day:
                        continue

                    if slot1.id in division_busy[(semester,division)]:
                        continue

                    if slot1.day in lab_day_used[(semester,division)]:
                        continue

                    faculty = None
                    for f in faculties:
                        if slot1.id not in faculty_busy[f.id] and slot2.id not in faculty_busy[f.id]:
                            faculty = f
                            break

                    if not faculty:
                        continue

                    room = None
                    for r in lab_rooms:
                        if slot1.id not in room_busy[r.id] and slot2.id not in room_busy[r.id]:
                            room = r
                            break

                    if not room:
                        continue

                    TimetableEntry.objects.create(
                        subject=subject,
                        faculty=faculty,
                        room=room,
                        timeslot=slot1,
                        semester=semester,
                        division=division,
                        is_lab=True
                    )

                    TimetableEntry.objects.create(
                        subject=subject,
                        faculty=faculty,
                        room=room,
                        timeslot=slot2,
                        semester=semester,
                        division=division,
                        is_lab=True
                    )

                    faculty_busy[faculty.id].update([slot1.id,slot2.id])
                    room_busy[room.id].update([slot1.id,slot2.id])
                    division_busy[(semester,division)].update([slot1.id,slot2.id])

                    lab_day_used[(semester,division)].add(slot1.day)

                    subject.lab_hours -= 2
                    created += 2

    # =================================================
    # LECTURE SCHEDULING
    # =================================================

    slots_random = list(TimeSlot.objects.filter(is_break=False))
    random.shuffle(slots_random)

    subjects_by_sem = {
        sem: list(Subject.objects.filter(semester=sem))
        for sem in semesters
    }

    subject_hours = {
        s.id: s.lecture_hours
        for sem in semesters
        for s in subjects_by_sem[sem]
    }

    remaining_hours = sum(subject_hours.values())

    attempts = 0
    max_attempts = 10000

    while remaining_hours > 0 and attempts < max_attempts:

        placed = False

        for slot in slots_random:

            for semester in semesters:
                for division in divisions:

                    if slot.id in division_busy[(semester,division)]:
                        continue

                    subjects = subjects_by_sem[semester]
                    random.shuffle(subjects)

                    for subject in subjects:

                        if subject_hours[subject.id] <= 0:
                            continue

                        faculties = faculty_map.get(subject.id, [])

                        faculty = None
                        for f in faculties:
                            if slot.id not in faculty_busy[f.id]:
                                faculty = f
                                break

                        if not faculty:
                            continue

                        room = None
                        for r in lecture_rooms:
                            if slot.id not in room_busy[r.id]:
                                room = r
                                break

                        if not room:
                            continue

                        TimetableEntry.objects.create(
                            subject=subject,
                            faculty=faculty,
                            room=room,
                            timeslot=slot,
                            semester=semester,
                            division=division,
                            is_lab=False
                        )

                        faculty_busy[faculty.id].add(slot.id)
                        room_busy[room.id].add(slot.id)
                        division_busy[(semester,division)].add(slot.id)

                        subject_hours[subject.id] -= 1
                        remaining_hours -= 1
                        created += 1

                        placed = True
                        break

                    if placed:
                        break
                if placed:
                    break
            if placed:
                break

        if not placed:
            break

        attempts += 1

    print("Total entries created:", created)


if __name__ == "__main__":
    generate_all_timetables()