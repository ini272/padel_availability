from datetime import datetime
import pytz
import requests
import json

# Define the URL
url = "https://playtomic.io/api/v1/availability"

# Define the time zones
utc_tz = pytz.utc
local_tz = pytz.timezone("Europe/Berlin")  # GMT+1 with daylight saving

def load_court_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def convert_time(date_str, time_str):
    utc_time_str = f"{date_str}T{time_str}"
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S")
    utc_time = utc_tz.localize(utc_time)
    local_time = utc_time.astimezone(local_tz)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

def create_overview_url(overview_name, tenant_id, date):
    base_url = "https://playtomic.io/"
    return f'{base_url}{overview_name}/{tenant_id}?q=PADEL~{date}'

def filter_suitable_slots(court):
    suitable_slots = []
    for slot in court["slots"]:
        local_start_time = convert_time(court["start_date"], slot["start_time"])
        if (datetime.strptime(local_start_time, "%Y-%m-%d %H:%M:%S").time()
                >= datetime.strptime("18:00:00", "%H:%M:%S").time()
                and slot["duration"] != 60):
            suitable_slots.append((local_start_time, slot["duration"], slot["price"]))
    return suitable_slots

def fetch_availability(venue, start_time, end_time):
    tenant_id = venue["tenant_id"]
    params = {
        "user_id": "me",
        "tenant_id": tenant_id,
        "sport_id": "PADEL",
        "local_start_min": start_time,
        "local_start_max": end_time,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        availability = response.json()
        for court in availability:
            court["suitable_slots"] = filter_suitable_slots(court)
        return availability
    else:
        print(f"Error: {response.status_code}")
        return []
