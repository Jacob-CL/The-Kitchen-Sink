import requests
from urllib.parse import urljoin
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

##########################################################################################################

def banner():
    return r"""
  ________  ________   __ __ __________________  _________   __   _____ _____   ____ __
 /_  __/ / / / ____/  / //_//  _/_  __/ ____/ / / / ____/ | / /  / ___//  _/ | / / //_/
  / / / /_/ / __/    / ,<   / /  / / / /   / /_/ / __/ /  |/ /   \__ \ / //  |/ / ,<   
 / / / __  / /___   / /| |_/ /  / / / /___/ __  / /___/ /|  /   ___/ // // /|  / /| |  
/_/ /_/ /_/_____/  /_/ |_/___/ /_/  \____/_/ /_/_____/_/ |_/   /____/___/_/ |_/_/ |_|  
                                                                                       

 [+] {0}
    """.format(time.ctime())

##########################################################################################################

# Function to check a URL and return its status code
def get_url_status_code(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code
    except requests.RequestException:
        return None  # Return None if there was an error making the request

##########################################################################################################

def enumerate_root_domain(root_domain, paths_file):
    print("\n--> Enumerating URL by checking for all response codes less than 400...\n")

    # Open the file containing the paths
    with open(paths_file, 'r') as file:
        paths = file.read().splitlines()

    valid_urls = []
    # Iterate over the paths from the file and check each one
    for path in paths:
        # Construct the full URL
        url = urljoin(root_domain, path)

        # Get the status code for the URL
        status_code = get_url_status_code(url)

        # Determine if the URL is valid based on the status code
        if status_code is not None and status_code < 400:
            print(f"{status_code} - Valid URL: {url}")
            valid_urls.append(url)  # Add the valid URL to the list
        else:
            # If status_code is None, it means the request failed
            if status_code is None:
                print(f"Error making request to: {url}")
            else:
                print(f"{status_code} ---- XX Invalid URL: {url}")
    
    print(f"\n✓✓ Enumeration on {root_domain} complete. \n")

##########################################################################################################

def search_for_HTML_comments(url):
    print("\n--> Searching for HTML comments in the page source...")
    # Define the list of strings you want to search for (start of HTML comments)
    search_strings = ['<!--']

    # Fetch the content of the URL
    try:
        response = requests.get(url)
        # Ensure the request was successful
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    # Split the content into lines for line-by-line examination
    content_lines = response.text.splitlines()

    # Iterate over each line in the content
    found = False  # Flag to track if any string is found

    for line_number, line in enumerate(content_lines, 1):
        # Check each string in the list
        for string in search_strings:
            if string in line:
                # Print the string, the line number, and the content of the line where the string is found
                print(f"\n✓✓ HTML Comments found on line {line_number}:\n {line.strip()}")
                found = True  # Set the flag to True if a string is found

    # After all lines have been checked, if no string was found, print the message
    if not found:
        print("\nXX No HTML comments found :(")

##########################################################################################################

def search_for_HTML_inputs(url):
    print("\n--> Searching for HTML input in the page source...")
    # Define the list of strings you want to search for (start of HTML comments)
    search_strings = ['<input', '<textarea', '<form']

    # Fetch the content of the URL
    try:
        response = requests.get(url)
        # Ensure the request was successful
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    # Split the content into lines for line-by-line examination
    content_lines = response.text.splitlines()

    # Iterate over each line in the content
    found = False  # Flag to track if any string is found

    for line_number, line in enumerate(content_lines, 1):
        # Check each string in the list
        for string in search_strings:
            if string in line:
                # Print the string, the line number, and the content of the line where the string is found
                print(f"\n✓✓ HTML inputs found on line {line_number}:\n {line.strip()}")
                found = True  # Set the flag to True if a string is found

    # After all lines have been checked, if no string was found, print the message
    if not found:
        print("\nXX No HTML inputs found :(")

##########################################################################################################

def search_for_javascript_tags(url):
    print("\n--> Searching for inline JavaScript <script> tags in the page source...")
    # Define the list of strings you want to search for (start of HTML comments)
    search_strings = ['<script']

    # Fetch the content of the URL
    try:
        response = requests.get(url)
        # Ensure the request was successful
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    # Split the content into lines for line-by-line examination
    content_lines = response.text.splitlines()

    # Iterate over each line in the content
    found = False  # Flag to track if any string is found

    for line_number, line in enumerate(content_lines, 1):
        # Check each string in the list
        for string in search_strings:
            if string in line:
                # Print the string, the line number, and the content of the line where the string is found
                print(f"\n✓✓ JavaScript tag found on line {line_number}:\n {line.strip()}")
                found = True  # Set the flag to True if a string is found

    # After all lines have been checked, if no string was found, print the message
    if not found:
        print("\nXX No JavaScript tags found :(")

##########################################################################################################

def search_for_frontend_filtering(url):
    print("\n--> Searching for evidence of front end filtering...")
    # Define the list of strings you want to search for (start of HTML comments)
    search_strings = ['dompurify', 'caja', 'sanitize', 'filter', 'addslashes', 'blacklist', 'black-list', 'black list']

    # Fetch the content of the URL
    try:
        response = requests.get(url)
        # Ensure the request was successful
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    # Split the content into lines for line-by-line examination
    content_lines = response.text.splitlines()

    # Iterate over each line in the content
    found = False  # Flag to track if any string is found

    for line_number, line in enumerate(content_lines, 1):
        # Check each string in the list
        for string in search_strings:
            if string in line:
                # Print the string, the line number, and the content of the line where the string is found
                print(f"\n✓✓ '{string}' mentioned on line {line_number}:\n {line.strip()}")
                found = True  # Set the flag to True if a string is found

    # After all lines have been checked, if no string was found, print the message
    if not found:
        print("\nXX No evidence of frontend XSS filtering tags found :)")

##########################################################################################################

def search_for_databases(url):
    print("\n--> Searching for evidence of databases...")
    # Define the list of strings you want to search for (start of HTML comments)
    search_strings = ['MySQL', 'Mongo', 'MSSQL', 'noSQL']

    # Fetch the content of the URL
    try:
        response = requests.get(url)
        # Ensure the request was successful
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    # Split the content into lines for line-by-line examination
    content_lines = response.text.splitlines()

    # Iterate over each line in the content
    found = False  # Flag to track if any string is found

    for line_number, line in enumerate(content_lines, 1):
        # Check each string in the list
        for string in search_strings:
            if string in line:
                # Print the string, the line number, and the content of the line where the string is found
                print(f"\n✓✓ '{string}' mentioned on line {line_number}:\n {line.strip()}s")
                found = True  # Set the flag to True if a string is found

    # After all lines have been checked, if no string was found, print the message
    if not found:
        print("\nXX No evidence of databases found :(")

##########################################################################################################

def load_patterns(pattern_file='CTFpatterns.txt'):
    """Load search patterns from the specified file."""
    try:
        with open(pattern_file, 'r', encoding='utf-8') as file:
            patterns = [line.strip() for line in file if line.strip()]
        return patterns
    except FileNotFoundError:
        print(f"Pattern file '{pattern_file}' not found.")
        exit(1)

def grep_files(directory, patterns):
    """Recursively search for patterns in files under the given directory."""
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file, 1):
                        for pattern in patterns:
                            if re.search(pattern, line):
                                print(f"✓✓ '{pattern}' found in {file_path} on line {line_num}")
            except UnicodeDecodeError:
                # Skipping binary or non-text files
                continue
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

##########################################################################################################

def count_interactable_inputs(url):
    options = Options()
    options.headless = True  # Set to False if you want to see the browser window
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Find all input elements
    elements = driver.find_elements(By.CSS_SELECTOR, "input, textarea")
    # Filter elements that are displayed and enabled (interactable)
    interactable_elements = [e for e in elements if e.is_displayed() and e.is_enabled()]

    if not interactable_elements:
        print("\nXX No interactable inputs found :(\n")
    else:
        print(f"\n✓✓ {len(interactable_elements)} interactable input(s) found.\n")

    #driver.quit()

    # driver.quit()

    # with open('payloads.txt', 'r') as file:
    #     payloads = file.read().splitlines()

    # for payload in payloads:
    #     for element in interactable_elements:
    #         element.send_keys(payload)

    # print(f"Entered payloads into {len(interactable_elements)} interactable inputs in {url}.")
