import requests
import json
from datetime import datetime, timedelta
import pytz
from tabulate import tabulate

# Load court IDs and venue information from the JSON file
with open('court_ids.json', 'r') as file:
    venues_data = json.load(file)

# Define the URL
url = 'https://playtomic.io/api/v1/availability'

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

def getAvailability(current_date):
    # Set the start and end times for the current date
    start_time = f"{current_date}T00:00:00"
    end_time = f"{current_date}T23:59:59"

    # Initialize results for the current date
    results = []

    # Loop through each venue
    for venue in venues_data['venues']:
        tenant_id = venue['tenant_id']
        court_names = venue['court_names']

        # Set the parameters
        params = {
            'user_id': 'me',
            'tenant_id': tenant_id,
            'sport_id': 'PADEL',
            'local_start_min': start_time,
            'local_start_max': end_time
        }

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
                        # Check if start time is after 6:00 PM and duration is not 60 minutes
                        if (datetime.strptime(local_start_time, "%Y-%m-%d %H:%M:%S").time() >= datetime.strptime("18:00:00", "%H:%M:%S").time() and
                            slot['duration'] != 60):
                            suitable_slots.append((local_start_time, slot['duration'], slot['price']))
                    if suitable_slots:
                        for slot in suitable_slots:
                            results.append([venue['name'], court_name, slot[0], slot[1], slot[2]])
        else:
            print(f'Error: {response.status_code}')
    return results

def printToConsole(all_results):
    # Print the results for each date in a table format
    for date, results in all_results.items():
        if results:
            # Add weekday to the header
            weekday = date.strftime("%A")
            headers = ["Venue", "Court", "Start Time", "Duration (minutes)", "Price (EUR)"]
            print(f"\nAvailability for {date} ({weekday}):\n")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print(f"\nNo suitable availability found for {date}.\n")

if __name__ == "__main__":
    # Get today's date
    today = datetime.now().date()

    # Store the results for all dates
    all_results = {}

    # Loop through the next thirteen days
    for i in range(14):
        # Calculate the current date
        current_date = today + timedelta(days=i)
        all_results[current_date] = getAvailability(current_date)

    printToConsole(all_results)
