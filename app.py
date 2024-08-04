from flask import Flask, render_template
from datetime import datetime, timedelta
from utils import load_court_data, convert_time, create_overview_url, fetch_availability

app = Flask(__name__)

# Load court IDs and venue information
venues_data = load_court_data("court_ids.json")

@app.route('/')
def home():
    today = datetime.now().date()
    all_results = {}

    for i in range(14):
        current_date = today + timedelta(days=i)
        start_time = f"{current_date}T00:00:00"
        end_time = f"{current_date}T23:59:59"
        all_results[current_date] = []

        for venue in venues_data["venues"]:
            availability = fetch_availability(venue, start_time, end_time)
            sorted_courts = sorted(
                availability,
                key=lambda x: (
                    list(venue["court_names"].values()).index(x["resource_id"])
                    if x["resource_id"] in venue["court_names"].values()
                    else float("inf")
                ),
            )

            for court in sorted_courts:
                court_id = court["resource_id"]
                court_name = next(
                    (name for name, cid in venue["court_names"].items() if cid == court_id),
                    court_id,
                )
                if "Single court" not in court_name:
                    for slot in court["suitable_slots"]:
                        overview_url = create_overview_url(venue["overview_name"], venue["tenant_id"], current_date.strftime("%Y-%m-%d"))
                        all_results[current_date].append(
                            [venue["name"], court_name, slot[0], slot[1], slot[2], overview_url]
                        )

    render_data = []
    for date, results in all_results.items():
        if results:
            weekday = date.strftime("%A")
            headers = ["Venue", "Court", "Start Time", "Duration (minutes)", "Price (EUR)", "Booking"]
            table_rows = [
                f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td><a href="{r[5]}" target="_blank">Book Here</a></td></tr>'
                for r in results
            ]
            table = f'<table><thead><tr>{" ".join([f"<th>{h}</th>" for h in headers])}</tr></thead><tbody>{" ".join(table_rows)}</tbody></table>'
            render_data.append((date, weekday, table))
        else:
            render_data.append((date, date.strftime("%A"), "No suitable availability found."))

    return render_template('index.html', data=render_data)

if __name__ == "__main__":
    app.run(debug=True)
