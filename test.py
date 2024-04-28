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

# color_options = {
#     "Blue": "#0000FF",
#     "Red": "#FF0000",
#     "Green": "#008000",
#     "Yellow": "#FFFF00",
#     "Purple": "#800080"
# }

# Add an event to the JSON file
def add_event_to_json(event_data):
    events = load_events()
    events.append(event_data)
    with open(EVENTS_FILE, 'w') as file:
        json.dump(events, file)
    st.success('Event added successfully!')

# Set up the Streamlit page
st.set_page_config(page_title="Habit Calendar", page_icon="📆")
st.title("Habit Calendar App")

# Initialize session state
if 'start_date' not in st.session_state:
    st.session_state['start_date'] = datetime.today()
if 'end_date' not in st.session_state:
    st.session_state['end_date'] = st.session_state['start_date']

# Display the event form with a submit button to ensure events can be added
with st.form("event_form"):
    st.subheader("Add Event")
    title = st.text_input("Event Title")

    # # Dropdown for color selection after the event title
    # color_name = st.selectbox(
    #     "Select Event Color",
    #     options=list(color_options.keys()),
    #     index=0,  # Default to the first option ("Blue")
    #     format_func=lambda x: f"{x}"  # This will show the color name in the dropdown
    # )
    # color_hex = color_options[color_name]  # Get the hex code of the selected color

    start_date = st.date_input("Start Date", key='start_date')
    start_time = st.time_input("Start Time", key='start_time')
    end_date = st.date_input("End Date", min_value=start_date, key='end_date')
    end_time = st.time_input("End Time", key='end_time')

    submit_button = st.form_submit_button("Add Event")

    if submit_button and title:
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)

        # Check if the end datetime is later than the start datetime
        if end_datetime <= start_datetime:
            # If there's a conflict, display a warning message
            st.error('The end date and time must be later than the start date and time.')
        else:
            event_data = {
                "title": title,
                "start": start_datetime.isoformat(),
                "end": end_datetime.isoformat(),
                "color": "#0000FF",  # Use the hex code for the event color
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
