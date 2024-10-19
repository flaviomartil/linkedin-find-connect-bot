import time
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

if not os.path.exists(".env"):
    print(".env file not found!")
    exit()

my_name = os.getenv("MY_NAME")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
keyword = os.getenv("KEYWORD")
location_keyword = os.getenv("LOCATION_KEYWORD", "")  # Default to empty string if not provided
send_with_note = os.getenv("SEND_WITH_NOTE")

if not my_name or not email or not password or not keyword:
    print("Please fill in all required fields in .env file!")
    exit()

# print welcome message
def print_green(text):
    print("\033[92m {}\033[00m".format(text))

def print_yellow(text):
    print("\033[93m {}\033[00m".format(text))

def print_red(text):
    print("\033[91m {}\033[00m".format(text))

# clear screen
os.system("cls" if os.name == "nt" else "clear")
print("\n----------------------------------")
print_green("Welcome to LinkedIn Auto Connect!")
print_yellow("Created by: klpod2211")
print("----------------------------------\n")
print_red("Note: Please read the following instructions carefully!")
print("1. Keyword is required and read from .env file (e.g: Software Engineer)")
print("2. Location is optional and also read from .env file")
print("3. 1 for Ha Noi, 2 for Ho Chi Minh, 3 for both, enter your GeoUrn Code (105790653,103697962) for other locations in the .env file")
print("4. If you want to stop the program, just press Ctrl + C\n")
print("----------------------------------\n")

# Prepare keywords for LinkedIn search URL
encoded_keywords = urllib.parse.quote_plus(keyword.replace(" | ", "|"))
# Check os and machine
path = "./drivers/"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Configure the correct ChromeDriver path based on OS
if platform.system() == "Windows":
    if os.path.exists(path + "chromedriver.exe"):
        path += "chromedriver.exe"
        options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    else:
        print("chromedriver.exe not found!")
        exit()
elif platform.system() == "Linux":
    if os.path.exists(path + "chromedriver"):
        path += "chromedriver"
    else:
        print("chromedriver not found!")
        exit()
elif platform.system() == "Darwin":
    if platform.machine() == "x86_64":
        if os.path.exists(path + "chromedriver"):
            path += "chromedriver"
        else:
            print("chromedriver not found!")
            exit()
    elif platform.machine() == "arm64":
        if os.path.exists(path + "chromedriver_arm64"):
            path += "chromedriver_arm64"
        else:
            print("chromedriver_arm64 not found!")
            exit()
    else:
        print("Unknown machine!")
        exit()
else:
    print("Unknown OS!")
    exit()

print(f"Using ChromeDriver from path: {path}")

s = Service(path)
driver = webdriver.Chrome(service=s, options=options)
driver.get("https://www.linkedin.com/login")
time.sleep(1)

driver.find_element(By.ID, "username").send_keys(email)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH, '//button[@type="submit"]').click()

time.sleep(2)

current_url = driver.current_url
if current_url.find("checkpoint") != -1:
    print_red("Please verify your login!")
    while True:
        time.sleep(1)
        current_url = driver.current_url
        if current_url.find("feed") != -1:
            break

print_green("Login successfully!")

# Set up the search URL with the formatted keywords
search_url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_keywords}&origin=SWITCH_SEARCH_VERTICAL"

print_green(f"Searching for {keyword} in {location_keyword if location_keyword else 'any location'}...")
print_green(f"Search URL: {search_url}")

driver.get(search_url)
time.sleep(2)

last_page_number = "100"

if not os.path.exists("./connections"):
    os.mkdir("./connections")

time_stamp = time.strftime("%Y%m%d-%H%M%S")
file_name = (
    keyword.replace(" ", "-")
    + "-"
    + (location_keyword or 'any-location').replace(" ", "-").replace(",", "-")
    + "-"
    + time_stamp
    + ".csv"
)
file_name = file_name.lower()

def close_modal():
    try:
        close_button = driver.find_element(By.XPATH, '//button[@aria-label="Dismiss"]')
        close_button.click()
        time.sleep(1)
    except:
        pass

def close_any_modals():
    try:
        close_modal_button = driver.find_element(By.XPATH, '//button[@aria-label="Dismiss"]')
        close_modal_button.click()
        time.sleep(1)
    except:
        pass

for i in range(int(last_page_number)):
    try:
        current_url = driver.current_url
        current_url = current_url.split("&page=")[0] + "&page=" + str(i + 1)
        driver.get(current_url)
        time.sleep(2)

        all_buttons = driver.find_elements(By.XPATH, "//button")
        connect_buttons = []
        for btn in all_buttons:
            try:
                if btn.find_element(By.XPATH, './span[text()="Connect"]'):
                    connect_buttons.append(btn)
            except:
                pass

        time.sleep(2)

        for btn in connect_buttons:
            btn_aria_label = btn.get_attribute("aria-label")
            user_name = btn_aria_label.split("Invite ")[1].split(" to connect")[0]
            span = driver.find_element(By.XPATH, f'//span[text()="{user_name}"]')
            parent = span.find_element(By.XPATH, "../..")
            user_url = parent.get_attribute("href").split("?")[0]

            try:
                btn.click()
            except ElementClickInterceptedException:
                close_any_modals()
                try:
                    btn.click()
                except ElementClickInterceptedException:
                    print_red(f"Could not click connect button for {user_name}. Skipping.")
                    continue

            print(f"Inviting {user_name} to connect...")
            time.sleep(2)

            if send_with_note == "true":
                send_connection_request_with_note = f"Hi {user_name},\nI'm {my_name}. Nice to connect!"
                driver.find_element(By.XPATH, '//button[@aria-label="Add a note"]').click()
                time.sleep(1)
                textarea = driver.find_element(By.XPATH, '//textarea[@name="message"]')
                textarea.send_keys(send_connection_request_with_note)
                driver.find_element(By.XPATH, '//button[@aria-label="Send"]').click()
            else:
                driver.find_element(By.XPATH, '//button[@aria-label="Send without a note"]').click()
                # Close the "Add a note to your invitation?" modal if it appears
                close_modal()

            with open(f"./connections/flavio", "a") as f:
                f.write(f"{user_name},{user_url}\n")
            time.sleep(2)
    except WebDriverException as e:
        print_red(f"An unexpected error occurred: {str(e)}. Skipping page {i + 1}.")
        continue
    except Exception as e:
        print_red(f"An unexpected error occurred: {str(e)}. Skipping page {i + 1}.")
        continue