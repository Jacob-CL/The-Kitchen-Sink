import requests
from urllib.parse import urljoin
import os
import re

# Function to save the page source to a local file
def save_page_source(url, content):
    # Use the URL path to create a meaningful filename
    filename = f"{sanitize_filename(url.replace('https://', ''))}.html"
    
    # Ensure the directory exists
    os.makedirs('{url}', exist_ok=True)
    full_path = os.path.join('{url}', filename)

    # Save the content to the file
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved valid page sources to {full_path}")



# Function to check a URL and return its status code
def get_url_status_code(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code
    except requests.RequestException:
        return None  # Return None if there was an error making the request



# Function to sanitize file names derived from URLs
def sanitize_filename(path):
    return path.strip("/").replace("/", "_") or "root"



# Function to save the page source to a local file
def save_page_source(url, content):
    # Use the URL path to create a meaningful filename
    filename = f"{sanitize_filename(url.replace('https://', ''))}.html"
    
    # Ensure the directory exists
    os.makedirs('Valid_URLs_source', exist_ok=True)
    full_path = os.path.join('Valid_URLs_source', filename)

    # Save the content to the file
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"> Saved page source to {full_path}")



def enumerate_and_save(root_domain, paths_file):
    print("Enumerating and finding valid URLs...")
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
            valid_urls.append(url)  # Add the valid URL to the list
    
    print("Saving valid URLs locally...")
    for valid_url in valid_urls:
        try:
            response = requests.get(valid_url)
            if response.status_code < 400:
                save_page_source(valid_url, response.text)
            else:
                print(f"Failed to fetch the page source for {valid_url}")
        except requests.RequestException as e:
            print(f"Error fetching page source for {valid_url}: {e}")



def enumerate_root_domain(root_domain, paths_file):
    # print("Checking for all response codes less than 400...")

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
                print(f"{status_code} ---- Invalid URL: {url}")
    
    print(f"\nConsider {root_domain} 3NUM3R4T3D!\n")


def search_for_HTML_comments(url):
    print("\nSearching for HTML comments in the page source...")
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
                print(f"HTML Comments found on line {line_number}: {line.strip()}")
                found = True  # Set the flag to True if a string is found

    # After all lines have been checked, if no string was found, print the message
    if not found:
        print("\n> No HTML comments found :(\n")

def search_for_javascript_tags(url):
    print("\nSearching for inline JavaScript <script> tags in the page source...")
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
                print(f"> JavaScript tag found on line {line_number}: {line.strip()}")
                found = True  # Set the flag to True if a string is found

    # After all lines have been checked, if no string was found, print the message
    if not found:
        print("\n> No JavaScript tags found :(\n")