# main.py
from bs4 import BeautifulSoup
import requests
from config import DISTRICT, CITIES
from models.powercut.powercut import getshutdown
from models.texts import outage_text
# from models.tnepds.tnepds import pds_setup
def main():
    # pds_setup()
    outage=getshutdown(DISTRICT)
    outage_text(outage, CITIES)

if __name__ == "__main__":
    main()