# main.py
from bs4 import BeautifulSoup
import requests
from config import DISTRICT, CITIES
from models.powercut import getshutdown
from models.texts import outage_text

def main():
    outage=getshutdown(DISTRICT)
    outage_text(outage, CITIES)

if __name__ == "__main__":
    main()