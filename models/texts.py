
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

def pds_text(data):
    messages = []
    
    # Ensure we got a dictionary, not a raw string
    if isinstance(data, str):
        import json
        data = json.loads(data)
    
    for group in data.get("entitlementDto", []):
        remaining_qty = group["entitledQuantity"] - group["currentQuantity"]
        if group["currentQuantity"] > 0:
            products = group["productList"]
            product_msgs = f'{products[0]["productName"]} {products[0]["productPrice"]} rupees quantity {group["currentQuantity"]} {products[0]["productUnit"]}'
            messages.append(product_msgs)
    final_message = "You still not bought " + ", ".join(messages)+" for this month in ration shop."

    if final_message.strip():   # avoid sending empty string
        print(final_message)
        speak(final_message)
    else:
        print("✅ All ration items already bought.")