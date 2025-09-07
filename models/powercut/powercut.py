import requests
from bs4 import BeautifulSoup
from config import POWER_BASE_URL
from models.powercut.ocrtotext import readocr
import json
import re

def getshutdown(dist="THENI"):
    session = requests.Session()
    # Step 1: Load the main page (session cookies will be set here)
    response = session.get(POWER_BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    options = {}
    zones=[]
    # Find the appcat select input dynamically
    select = soup.find("select", {"id": lambda v: v and v.endswith(":appcat_input")})
    if not select:
        raise ValueError("Could not find select element for appcat_input")
    ses=select['id'].split(":")[0]
    print("Uses: "+ses)
    for opt in select.find_all("option"):
        value = opt.get("value", "").strip()
        label = opt.get_text(strip=True)
        options[label] = value
        if label!='--Select All--':
            zones.append(label)
    print("Available district(zone) names:", zones)
    # Step 2: Extract captcha image URL
    captcha_tag = soup.find("img", {"id": ses+":imgCaptchaId"})
    captcha_url = "https://www.tnebltd.gov.in/outages/" + captcha_tag["src"]
    # print("Captcha URL:", captcha_url)
    # Step 3: Download captcha
    captcha_img = session.get(captcha_url)
    with open("captcha.jpg", "wb") as f:
        f.write(captcha_img.content)
    text = readocr("captcha.jpg")
    # Extract hidden ViewState
    viewstate = soup.find("input", {"name": "javax.faces.ViewState"})["value"]
    # Example form data (you must OCR the captcha before filling!)
    form_data = {
        ses: ses,
        ses+":appcat_input": options[dist],   # Example: CBE/METRO
        ses+":cap": text,          # OCR or user input
        "javax.faces.ViewState": viewstate,
        ses+":submit3": "Submit"
    }
    # Post request
    post_resp = session.post(POWER_BASE_URL, data=form_data)
    post_soup = BeautifulSoup(post_resp.text, "html.parser")
    viewstate2 = post_soup.find("input", {"name": "javax.faces.ViewState"})["value"]
    update_div = post_soup.find(attrs={"id": re.compile(r"^j_idt\d+:j_idt\d+$")})
    if not update_div:
        raise ValueError("Could not find outage update container ID")
    # print(post_resp.text)
    outage_id=update_div['id']
    # print(outage_id,"update div")
    url = "https://www.tnebltd.gov.in/outages/index1.xhtml"
    # First load to capture cookies
    session.get(url)
    # Then XHR request
    data_resp = session.post(url, data={
        "javax.faces.partial.ajax": "true",
        "javax.faces.source": outage_id,
        "javax.faces.partial.execute": outage_id,
        "javax.faces.partial.render": outage_id,
        outage_id: outage_id,
        "javax.faces.ViewState": viewstate2
    })
    return parse_outage_response(data_resp.text, outage_id)



def parse_outage_response(xml_text, outage_id):
    # Parse as XML (not HTML!)
    soup = BeautifulSoup(xml_text, "xml")

    # Find the table inside CDATA
    cdata_section = soup.find("update", {"id": outage_id})
    if not cdata_section:
        return {"error": "No update section found"}

    # Parse the CDATA as HTML now
    inner_html = BeautifulSoup(cdata_section.text, "html.parser")
    table = inner_html.find("table")
    if not table:
        return {"error": "No table found"}

    # Extract rows
    rows = []
    for tr in table.find_all("tr")[1:]:  # skip header
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cols:
            rows.append({
                "date": cols[0],
                "town": cols[1],
                "substation": cols[2],
                "feeder": cols[3],
                "location": cols[4],
                "type_of_work": cols[5],
                "from_time": cols[6],
                "to_time": cols[7]
            })

    return rows
