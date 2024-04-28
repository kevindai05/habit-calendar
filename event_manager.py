# # event_manager.py

# import streamlit as st
# from datetime import datetime

# def add_event(events):
#     st.header("Add a New Event")
    
#     # Friendly names and corresponding hex codes for colors
#     color_options = {
#         "Blue": "#4B86B4",
#         "Green": "#8CC152",
#         "Red": "#FF4B4B",
#         "Yellow": "#FFC65C",
#         "Purple": "#B48CF4"
#     }

#     title = st.text_input("Event Title", "")
#     color_name = st.selectbox("Event Color", options=list(color_options.keys()), index=0)
#     color = color_options[color_name]

#     start_datetime = st.time_input("Start Time", datetime.now())
#     end_datetime = st.time_input("End Time", datetime.now())

#     start_date = st.date_input("Start Date", datetime.now())
#     end_date = st.date_input("End Date", datetime.now())

#     start = datetime.combine(start_date, start_datetime).isoformat()
#     end = datetime.combine(end_date, end_datetime).isoformat()

#     if st.button("Add Event"):
#         events.append({
#             "title": title,
#             "color": color,
#             "start": start,
#             "end": end,
#             "resourceId": "a"
#         })
#         st.success("Event added successfully!")
#         st.experimental_rerun()

import json

def add_event(events, event_data):
    """Add an event to the event list and save it to a JSON file."""
    # Append the new event to the events list
    events.append(event_data)
    
    # Save the updated events list to a JSON file
    with open('events.json', 'w') as file:
        json.dump(events, file)
    
    return "Event added successfully!"
