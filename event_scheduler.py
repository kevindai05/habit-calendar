import json
from datetime import datetime, timedelta

def load_events():
    with open('events.json', 'r') as file:
        return json.load(file)

def save_events(events):
    with open('events.json', 'w') as file:
        json.dump(events, file, indent=4, default=str)

def add_habit_to_calendar(name, desc, color, start_date, end_date, start_time, end_time, duration, times_week, times_day):
    events = load_events()
    # Convert start_date and end_date directly to datetime.date objects
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Use start_time and end_time directly as datetime.time objects if they are strings
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%H:%M").time()
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%H:%M").time()

    duration = timedelta(minutes=duration)

    # Generate potential event start times
    delta_days = (end_date - start_date).days + 1
    potential_starts = []
    for day in range(delta_days):
        current_date = start_date + timedelta(days=day)
        current_time = datetime.combine(current_date, start_time)
        while current_time.time() <= end_time:
            potential_starts.append(current_time)
            current_time += duration

    # Filter potential starts that do not conflict
    valid_starts = []
    for potential_start in potential_starts:
        conflict = False
        potential_end = potential_start + duration
        for event in events:
            event_start = datetime.fromisoformat(event['start'])
            event_end = datetime.fromisoformat(event['end'])
            if not (potential_end <= event_start or potential_start >= event_end):
                conflict = True
                break
        if not conflict:
            valid_starts.append(potential_start)

    # Distribute events across available slots
    used_starts = []
    for _ in range(times_week):
        for _ in range(times_day):
            if valid_starts:
                start_time = valid_starts.pop(0)
                end_time = start_time + duration
                event_data = {
                    "title": name,
                    "description": desc,
                    "color": color,
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat()
                }
                events.append(event_data)
                used_starts.append(start_time)

    save_events(events)
    return f'{len(used_starts)} events successfully added!'
