import json
from padel_availability import *
from datetime import datetime, timedelta

def check_availability(event, context):
    body = {
        "message": "Go Serverless v2.0! Your function executed successfully!",
        "input": event,
    }

    today = datetime.now().date()
    availability = getAvailability(today + timedelta(1))
    return {"statusCode": 200, "body": json.dumps(list(availability))}

print(check_availability("", ""))
