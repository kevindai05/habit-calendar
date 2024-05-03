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
    # Ensure date and time types are correct
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%H:%M").time()
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%H:%M").time()

    duration_delta = timedelta(minutes=duration)

    # Generate potential event start times
    delta_days = (end_date - start_date).days + 1
    potential_starts = {}
    for day in range(delta_days):
        day_date = start_date + timedelta(days=day)
        current_time = datetime.combine(day_date, start_time)
        daily_starts = []
        while current_time.time() <= end_time:
            if (datetime.combine(day_date, end_time) - current_time) >= duration_delta:
                daily_starts.append(current_time)
            current_time += timedelta(minutes=15)  # Increment by a smaller step to check more slots
        potential_starts[day_date] = daily_starts

    # Filter potential starts that do not conflict and respect daily limits
    valid_starts = {}
    for day, starts in potential_starts.items():
        valid_starts[day] = []
        for potential_start in starts:
            conflict = False
            potential_end = potential_start + duration_delta
            for event in events:
                event_start = datetime.fromisoformat(event['start'])
                event_end = datetime.fromisoformat(event['end'])
                # Check for overlapping events
                if (potential_start < event_end and potential_end > event_start):
                    conflict = True
                    break
            if not conflict:
                valid_starts[day].append(potential_start)

    # Distribute events across available slots respecting daily limits
    used_starts = []
    for day, starts in valid_starts.items():
        count_per_day = 0
        for start_time in starts:
            if count_per_day < times_day:
                end_time = start_time + duration_delta
                event_data = {
                    "title": name,
                    "description": desc,
                    "color": color,
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat()
                }
                events.append(event_data)
                used_starts.append(start_time)
                count_per_day += 1
            if count_per_day >= times_day:
                break

    save_events(events)
    return f'{len(used_starts)} events successfully added!'
