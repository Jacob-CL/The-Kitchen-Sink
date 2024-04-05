# Custom function for static analysis
def static_analysis(url):
    # Placeholder for your static analysis logic
    print(f"--> Conducting static analysis..")
    # HTML input fields
    # HTML comments
    # JavaScript tags
    # Evidence of Frontend filtering 
    # Evidence of Databases

import requests
from urllib.parse import urljoin
import os
import re
import time

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
                print(f"\n✓✓ JavaScript tag found on line {line_number}:\n {line.strip()}\n")
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
    search_strings = ['MySQL', 'Mongo', 'MSSQL']

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


##########################################################################################################