import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SyncSchedule.settings")
django.setup()

from generator.models import TimeSlot


# Clear old slots
TimeSlot.objects.all().delete()


days = ["MON", "TUE", "WED", "THU", "FRI"]

start_time = datetime.strptime("08:30", "%H:%M")
end_time = datetime.strptime("15:30", "%H:%M")

break_start = datetime.strptime("12:30", "%H:%M")
break_end = datetime.strptime("13:30", "%H:%M")

slot_duration = timedelta(hours=1)

count = 0

for day in days:

    current = start_time

    while current < end_time:

        next_time = current + slot_duration

        is_break = False
        if current == break_start:
            is_break = True

        TimeSlot.objects.create(
            day=day,
            start_time=current.time(),
            end_time=next_time.time(),
            is_break=is_break
        )

        current = next_time
        count += 1


print(f" {count} timeslots inserted successfully!")