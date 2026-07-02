import requests
import csv
import os
from datetime import datetime

appointments = [
    ("17.", "https://okticket.de/index.php?pmp_id=43189&event_id=55846"),
    ("18.", "https://okticket.de/index.php?pmp_id=43190&event_id=55847"),
    ("23.", "https://okticket.de/index.php?pmp_id=43191&event_id=55848"),
    ("24.", "https://okticket.de/index.php?pmp_id=43192&event_id=55849"),
    ("25.", "https://okticket.de/index.php?pmp_id=43193&event_id=55850"),
]

#CSV_FILE = "/volume1/homes/jonas/scripts/ticket_history.csv"
CSV_FILE = "/volume1/web/data/ticket_history.csv"

def count_occupied(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.text.lower().count("occupied")
    except:
        return -1


def collect_counts():
    counts = []
    for _, url in appointments:
        counts.append(count_occupied(url))
    return counts


def write_csv():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    counts = collect_counts()

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header nur einmal schreiben
        if not file_exists:
            header = ["timestamp"] + [date for date, _ in appointments]
            writer.writerow(header)

        writer.writerow([timestamp] + counts)


if __name__ == "__main__":
    write_csv()
