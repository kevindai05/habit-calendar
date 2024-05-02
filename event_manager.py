import json

def add_event(events, event_data):
    """Add an event to the event list and save it to a JSON file."""
    # Append the new event to the events list
    events.append(event_data)
    
    # Save the updated events list to a JSON file
    with open('events.json', 'w') as file:
        json.dump(events, file)
    
    return "Event added successfully!"
