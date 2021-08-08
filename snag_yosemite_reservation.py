import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from server import server_main

parser = argparse.ArgumentParser()
parser.add_argument("--date")
parser.add_argument("--server", action='store_true')
args = parser.parse_args()
if args.server is not None:
    server_main()
    exit(0)
if args.date == None:
   parser.error('Specify date as --date=\"<Day of week>, <Month><Date>, <Year>\"')

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get("https://www.recreation.gov/timed-entry/10086745/ticket/10086746")
driver.find_element_by_id('tourCalendarWithKey').click()

reservations_available = True
try:
    driver.find_element_by_css_selector(f"td[aria-label=\"{args.date}, available\"]").click()
except NoSuchElementException:
    reservations_available = False

if reservations_available:
    print("YES - reservations available :)")
else:
    print("NO - reservations not available :(")

driver.close()
