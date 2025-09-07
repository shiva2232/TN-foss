import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

POWER_BASE_URL = "https://www.tnebltd.gov.in/outages/viewshutdown.xhtml"
CITIES=["cumbum"] # remove everything in this list and add you city name(enter only in lowercase letters)
DISTRICT="THENI" # Your zone(sub district) name
MOBILE_PDS=str(os.getenv("MOBILE_NUMBER")) # mobile number without +91
DEVICE_NUMBER=str(os.getenv("DEVICE_NUMBER"))
VOICE_DIR="voice/en_GB-alba-medium.onnx"