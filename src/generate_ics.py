import requests
from icalendar import Calendar, Event
from datetime import datetime
import os

# URL dell'API EasyPark
url = "https://webapi.easypark24.com/api/Event/GetEvent?ListParkings=1123&ListParkings=1130"

# Richiesta HTTP
response = requests.get(url)
data = response.json()

# Crea il calendario
calendar = Calendar()

# Aggiungi eventi
for item in data:
    try:
        event = Event()
        event.add('summary', item.get("Title", "Evento EasyPark"))

        start_str = item.get("StartDate")
        end_str = item.get("EndDate")

        if start_str and end_str:
            start_dt = datetime.fromisoformat(start_str)
            end_dt = datetime.fromisoformat(end_str)
            event.add('dtstart', start_dt)
            event.add('dtend', end_dt)
            calendar.add_component(event)
    except Exception as e:
        print(f"Errore nell'elaborazione di un evento: {e}")

# Assicurati che la cartella docs esista
os.makedirs("docs", exist_ok=True)

# Scrivi il file .ics
with open("docs/sansirocalendar.ics", "wb") as f:
    f.write(calendar.to_ical())

