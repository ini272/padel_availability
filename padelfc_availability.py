import requests
from datetime import datetime, timedelta
import pytz

# Define the URL
url = 'https://playtomic.io/api/v1/availability'

# Define the parameters
params = {
    'user_id': 'me',
    'tenant_id': '0220b0b5-c27a-4433-9c91-1798aaec5250',
    'sport_id': 'PADEL'
}

# Mapping of court IDs to their names, sorted by court names
court_names = {
    'Court 1': 'eb3c33f1-8c59-4330-88dc-1f195745c6de',
    'Court 2': '71394e66-2022-4797-a5da-c9ca9abc9d1a',
    'Court 3': 'f0ed2970-d8f4-42a5-a6f1-bb0b0e6328eb',
    'Court 4': '35ec3445-605b-41a1-ba95-da09cf6b1065',
    'Court 5': 'c8c86813-c7ca-4621-a2f4-ee338073cb77',
    'Outdoor spree 1': '932517be-94a0-4752-bd4c-62b249449659',
    'Outdoor spree 2': '18aa889f-9bfd-4ded-8e91-ee93d74f49a2',
    'Single court 1': '0fe7e91d-46c6-4b11-92b3-c16a7cc1b1d2',
    'Single court 2': '5f285a16-c9dc-4544-99b7-1c56cfbb9002'
}

# Define the time zones
utc_tz = pytz.utc
local_tz = pytz.timezone('Europe/Berlin')  # GMT+1 with daylight saving

# Function to convert time
def convert_time(date_str, time_str):
    # Combine date and time
    utc_time_str = f"{date_str}T{time_str}"
    # Parse into datetime
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S")
    # Localize to UTC
    utc_time = utc_tz.localize(utc_time)
    # Convert to local time
    local_time = utc_time.astimezone(local_tz)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

# Get today's date
today = datetime.now().date()

# Loop through the next thirteen days
for i in range(5):
    # Calculate the current date
    current_date = today + timedelta(days=i)

    # Set the start and end times for the current date
    start_time = f"{current_date}T00:00:00"
    end_time = f"{current_date}T23:59:59"

    # Set the start and end times in the parameters
    params['local_start_min'] = start_time
    params['local_start_max'] = end_time

    # Perform the GET request
    response = requests.get(url, params=params)

    # Check the response
    if response.status_code == 200:
        availability = response.json()

        # Sort courts by their order
        sorted_courts = sorted(availability, key=lambda x: list(court_names.values()).index(x['resource_id']) if x['resource_id'] in court_names.values() else float('inf'))

        for court in sorted_courts:
            court_id = court['resource_id']
            court_name = next((name for name, cid in court_names.items() if cid == court_id), court_id)
            if "Single court" not in court_name:
                suitable_slots = []
                for slot in court['slots']:
                    local_start_time = convert_time(court['start_date'], slot['start_time'])
                    # Check if start time is after 6:00 PM
                    if datetime.strptime(local_start_time, "%Y-%m-%d %H:%M:%S").time() >= datetime.strptime("18:00:00", "%H:%M:%S").time():
                        suitable_slots.append(slot)
                if suitable_slots:
                    print(f"Court: {court_name}")
                    print(f"Date: {court['start_date']}")
                    for slot in suitable_slots:
                        local_start_time = convert_time(court['start_date'], slot['start_time'])
                        print(f"  - Start Time: {local_start_time}, Duration: {slot['duration']} minutes, Price: {slot['price']}")
                    print("\n")
    else:
        print(f'Error: {response.status_code}')

