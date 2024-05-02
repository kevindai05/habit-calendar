import json
from datetime import datetime, timedelta, date, time
import streamlit as st

EVENTS_FILE = 'events.json'

def add_habit_to_calendar(name, desc, color, start_date, end_date, start_time, end_time, duration, buffer, times_week, times_day, diagnostics):
    # Function implementation...
    pass

def load_events():
    try:
        with open(EVENTS_FILE, 'r') as file:
            events = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []
    return events

def save_events(events):
    with open(EVENTS_FILE, 'w') as file:
        json.dump(events, file)

def is_slot_available(start_datetime, duration, buffer, events, diagnostics):
    end_datetime = start_datetime + timedelta(minutes=duration)
    for event in events:
        event_start = datetime.fromisoformat(event['start'])
        event_end = datetime.fromisoformat(event['end'])
        if not (end_datetime + timedelta(minutes=buffer) <= event_start or 
                start_datetime - timedelta(minutes=buffer) >= event_end):
            diagnostics.append(f"Conflict found: Slot from {start_datetime} to {end_datetime} conflicts with existing event from {event_start} to {event_end}.")
            return False
    return True

def generate_day_slots(date, start_time, end_time, duration, buffer, events, diagnostics):
    available_slots = []
    current_time = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)
    while current_time + timedelta(minutes=duration) <= end_datetime:
        if is_slot_available(current_time, duration, buffer, events, diagnostics):
            available_slots.append(current_time)
        current_time += timedelta(minutes=duration + buffer)
    diagnostics.append(f"Generated slots for {date}: {available_slots}")
    return available_slots

def find_available_slots(start_date, end_date, start_time, end_time, duration, buffer, events, diagnostics):
    slots = {}
    current_date = start_date
    while current_date <= end_date:
        day_slots = generate_day_slots(current_date, start_time, end_time, duration, buffer, events, diagnostics)
        if day_slots:
            slots[current_date] = day_slots
        current_date += timedelta(days=1)
    return slots

def add_habit_to_calendar(name, desc, color, start_date, end_date, start_time, end_time, duration, buffer, times_week, times_day, diagnostics):
    events = load_events()
    available_slots = find_available_slots(start_date, end_date, start_time, end_time, duration, buffer, events, diagnostics)
    events_planned = 0

    for date, day_slots in available_slots.items():
        for slot in day_slots:
            daily_event_count = sum(1 for event in events if datetime.fromisoformat(event['start']).date() == slot.date())
            if daily_event_count >= times_day:
                diagnostics.append(f"Daily limit reached for {date}.")
                continue
            if events_planned >= times_week:
                diagnostics.append("Weekly limit reached.")
                break
            events.append(create_event(name, desc, color, slot, duration))
            events_planned += 1

    save_events(events)
    if events_planned < times_week:
        return f"Managed to schedule only {events_planned} out of {times_week} required events due to lack of available slots."
    return "Events scheduled successfully."

def create_event(name, desc, color, start_datetime, duration):
    end_datetime = start_datetime + timedelta(minutes=duration)
    return {
        "title": name,
        "description": desc,
        "color": color,
        "start": start_datetime.isoformat(),
        "end": end_datetime.isoformat()
    }

# Streamlit app code (place this part in your main app logic)
diagnostics = []
# Example button in Streamlit to trigger scheduling
if st.button("Schedule Event"):
    diagnostics = []  # Initialize diagnostics list
    message = add_habit_to_calendar(
        "Read a Book", "Enjoy reading", "#FF5733",
        date(2024, 5, 13), date(2024, 5, 17),
        time(12, 0), time(18, 0), 15, 0, 4, 1, diagnostics
    )
    st.success(message)
    for diag in diagnostics:
        st.write(diag)

