import streamlit as st
from datetime import datetime, time, timedelta
import json
from streamlit_calendar import calendar

# Define the path to the JSON file for events
EVENTS_FILE = 'events.json'

# Load events from the JSON file
def load_events():
    try:
        with open(EVENTS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty list if there are problems loading the file
        return []

# Color options for events
color_options = {
    "Blue": "#0000FF",
    "Red": "#FF0000",
    "Green": "#008000",
    "Yellow": "#FFFF00",
    "Purple": "#800080"
}

# Add an event to the JSON file
def add_event_to_json(event_data):
    events = load_events()
    events.append(event_data)
    with open(EVENTS_FILE, 'w') as file:
        json.dump(events, file)
    st.success('Event added successfully!')

# Clear json file
def clear_all_events():
    with open(EVENTS_FILE, 'w') as file:
        json.dump([], file)  # Write an empty list to the file
    st.success('All events have been cleared.')

# Set up the Streamlit page
st.set_page_config(page_title="Habit Calendar", page_icon="📆")
st.title("Habit Calendar App")

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
    # Show or hide time inputs based on all_day_event checkbox state
    start_date = st.date_input("Start Date", key='start_date')
    end_date = st.date_input("End Date", key='end_date', min_value=start_date)
    
    if not all_day_event:
        start_time = st.time_input("Start Time", key='start_time')
        end_time = st.time_input("End Time", key='end_time')
    else:
        # Hide time inputs and reset their values when all day event is checked
        start_time = time.min
        end_time = time.max
        st.session_state['start_time'] = start_time
        st.session_state['end_time'] = end_time

    submit_button = st.form_submit_button("Add Event")

    if submit_button and title:
        # Combine dates and times into datetime objects
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)

        # Validation and event addition logic
        if end_datetime < start_datetime:
            st.error('The end date and time must be later than the start date and time.')
        else:
            st.error('')  # Clear any previous error messages
            event_data = {
                "title": title,
                "start": start_datetime.isoformat(),
                "end": (end_datetime + timedelta(days=1)).isoformat(),  # Include the end date in the span
                "color": color_hex,
                "allDay": all_day_event
            }
            add_event_to_json(event_data)

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