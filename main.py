# 1. Imports
import streamlit as st
from datetime import datetime, time, timedelta
import json
from streamlit_calendar import calendar

# 2. Constants

# Define the path to the JSON file for events
EVENTS_FILE = 'events.json'

# Color options for events
color_options = {
    "Blue": "#0000FF",
    "Red": "#FF0000",
    "Green": "#008000",
    "Yellow": "#FFFF00",
    "Purple": "#800080"
}

constant_events = [
    {"title": "IMB Class", "start": "2024-05-17T09:00:00", "end": "2024-05-17T12:00:00", "color": "#800080"},
    {"title": "Lunch", "start": "2024-05-13T12:00:00", "end": "2024-05-13T13:00:00", "color": "#008000"},
    {"title": "TED Talk", "start": "2024-05-13T13:30:00", "end": "2024-05-13T17:00:00", "color": "#0000FF"},
    {"title": "Dinner", "start": "2024-05-15T18:00:00", "end": "2024-05-15T19:00:00", "color": "#008000"},
    {"title": "Dinner", "start": "2024-05-13T18:00:00", "end": "2024-05-13T19:00:00", "color": "#008000"},
    {"title": "Broadway Show", "start": "2024-05-13T19:00:00", "end": "2024-05-13T22:00:00", "color": "#0000FF"},
    {"title": "Lunch", "start": "2024-05-15T12:00:00", "end": "2024-05-15T13:00:00", "color": "#008000"},
    {"title": "Lunch", "start": "2024-05-14T12:00:00", "end": "2024-05-14T13:00:00", "color": "#008000"},
    {"title": "Product Management Class", "start": "2024-05-15T13:00:00", "end": "2024-05-15T15:00:00", "color": "#800080"},
    {"title": "Cleaning the house", "start": "2024-05-15T15:15:00", "end": "2024-05-15T16:15:00", "color": "#800080"},
    {"title": "Psychology Class", "start": "2024-05-14T16:00:00", "end": "2024-05-14T19:00:00", "color": "#800080"},
    {"title": "Family Call", "start": "2024-05-14T14:15:00", "end": "2024-05-14T15:15:00", "color": "#800080"},
    {"title": "Lunch", "start": "2024-05-16T12:00:00", "end": "2024-05-16T13:00:00", "color": "#008000"},
    {"title": "Lunch", "start": "2024-05-17T12:00:00", "end": "2024-05-17T13:00:00", "color": "#008000"},
    {"title": "Negotiation Class", "start": "2024-05-16T13:00:00", "end": "2024-05-16T15:00:00", "color": "#800080"},
    {"title": "Job Interview", "start": "2024-05-17T14:00:00", "end": "2024-05-17T16:00:00", "color": "#0000FF"},
    {"title": "Prepare for dinner", "start": "2024-05-16T17:00:00", "end": "2024-05-16T17:30:00", "color": "#800080"},
    {"title": "Senior Dinner", "start": "2024-05-16T18:00:00", "end": "2024-05-16T20:00:00", "color": "#008000"},
    {"title": "Flight to New York", "start": "2024-05-18T12:00:00", "end": "2024-05-18T19:00:00", "color": "#0000FF"},
]

# 3. Function Definitions

# Load events from the JSON file
def load_events():
    try:
        with open(EVENTS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty list if there are problems loading the file
        return []

# Add an event to the JSON file
def add_event_to_json(event_data):
    events = load_events()
    events.append(event_data)
    # Save events in JSON
    with open(EVENTS_FILE, 'w') as file:
        json.dump(events, file)
    st.success('Event added successfully!')
    # st.experimental_rerun()  # Rerun the app to refresh data

# Clear json file
def clear_all_events():
    # Write constant events to the file
    with open(EVENTS_FILE, 'w') as file:
        json.dump(constant_events, file)
    st.success('All events have been cleared and default events restored.')

# 4. Streamlit Config

# Set up the Streamlit page
st.set_page_config(page_title="Habit Calendar", page_icon="📆")
st.title("Habit Calendar App")

# 5. Main Code Interface

# Event form with validation
with st.form("event_form"):
    st.subheader("Add Event")
    title = st.text_input("Event Title")

    # Checkbox for all-day event
    all_day_event = st.checkbox("All Day Event")

    # Dropdown for color selection
    color_name = st.selectbox(
        "Select Event Color",
        options=list(color_options.keys()),
        index=0,  # Default to the first option ("Blue")
    )
    color_hex = color_options[color_name]

    # Input fields for date and time
    start_date = st.date_input("Start Date", key='start_date')
    end_date = st.date_input("End Date", key='end_date', min_value=start_date)
    
    if not all_day_event:
        start_time = st.time_input("Start Time", key='start_time')
        end_time = st.time_input("End Time", key='end_time')
    else:
        # For all-day events, the time is set to the full day
        start_time = time.min
        end_time = time.max

    submit_button = st.form_submit_button("Add Event")

    if submit_button and title:
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)
        
        if not all_day_event:
            # Normal event, no need to adjust end_datetime
            if end_datetime < start_datetime:
                st.error('The end date and time must be later than the start date and time.')
            else:
                event_data = {
                    "title": title,
                    "start": start_datetime.isoformat(),
                    "end": end_datetime.isoformat(),
                    "color": color_hex,
                    "allDay": all_day_event
                }
                add_event_to_json(event_data)
        else:
            # Adjust end_datetime to the end of the day for all-day events
            end_datetime = datetime.combine(end_date, time.max)
            event_data = {
                "title": title,
                "start": start_datetime.isoformat(),
                "end": end_datetime.isoformat(),
                "color": color_hex,
                "allDay": all_day_event
            }
            add_event_to_json(event_data)

# Clear calendar
if st.button('Clear All Events'):
    clear_all_events()

if st.button('Refresh Page'):
    # This line will rerun the entire script, refreshing the page
    st.experimental_rerun()

# Calendar component
st.subheader('Calendar')
events = load_events()  # Load events for the calendar

calendar_options = {
    "locale": "en",
    "selectable": True,
    "initialView": "dayGridMonth",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridDay,timeGridWeek,dayGridMonth"
    }
}

# Display the calendar with events
calendar_result = calendar(events=events, options=calendar_options, key="calendar")

# Debug information if needed
st.write(calendar_result)

# How to push code to Github:

# git pull --rebase origin main
# git add .
# git commit -m "Your commit message here"
# git push origin main