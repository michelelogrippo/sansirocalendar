import requests
from icalendar import Calendar, Event
from datetime import datetime, timedelta
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
        event.add('summary', item.get("Description"))

        start_time_str = item.get("Time")
        event_date_str = item.get("IdParkings")[0].get("FromDate")[0:10]  # Prendi solo la parte della data
        
        # Converti la stringa in un oggetto datetime
        start_str = event_date_str + " " + start_time_str


        if start_str:
            start_dt = datetime.fromisoformat(start_str)
            end_dt = start_dt + timedelta(hours=2)
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

