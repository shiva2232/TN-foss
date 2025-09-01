
from models.speak import speak
from datetime import datetime

def outage_text(outage, keywords):
    success=False;
    for entry in outage:
        town_lower = entry['town'].lower()
        if any(keyword in town_lower for keyword in keywords):
            success=True
            # Convert 24-hour format to "morning/evening" style
            from_hour = int(entry['from_time'].split(':')[0])
            to_hour = int(entry['to_time'].split(':')[0])
            from_period = "morning" if from_hour < 12 else "afternoon"
            to_period = "morning" if to_hour < 12 else "evening"
            date_obj = datetime.strptime(entry['date'], "%d-%m-%Y")
            day_of_week = date_obj.strftime("%A")
            speak(f"We found city {entry['town']} is power outage on coming {day_of_week} {entry['date']} "
                  f"between {from_period} {entry['from_time']} to {to_period} {entry['to_time']} "
                  f"due to {entry['type_of_work']}. Please charge your devices.")
    if not success:
            speak("No power outage in this week.")