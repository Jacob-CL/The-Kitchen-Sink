import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import socket
import nmap
import dns.resolver
from urllib.parse import urlparse, urljoin

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

def directorywalk(root_domain, paths_file):
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
    
    print(f"\n✓✓ Directory walk enumeration on {root_domain} complete. \n")

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

    test_string = r"JL;:!--''\" <SCs>=&{[(`)]}//JL"
    test_string_pattern = r"JL.{0,26}JL"

    options = Options()
    options.headless = True  # Set to False if you want to see the browser window
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Scroll to the bottom of the page - be careful of infinite scroll websites here
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Find all input elements
    elements = driver.find_elements(By.CSS_SELECTOR, "input, textarea")
    # Filter elements that are displayed and enabled (interactable)
    interactable_elements = [e for e in elements if e.is_displayed() and e.is_enabled()]

    if not interactable_elements:
        print("""\nXX No interactable inputs found :(
              Note: Prone to false negatives - this script may not have done enough to make the inputs interactable.\n""")
    else:
        print(f"\n✓✓ {len(interactable_elements)} interactable input(s) found.\n")

        for element in elements:
            if element.is_displayed() and element.is_enabled():
                # Clear the input field and enter the test string
                # element.clear()
                element.send_keys(test_string)

                # Attempt to submit the form
                element.send_keys(Keys.RETURN)
                
                # Wait for the page to reload or for a response to be received
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState;") == "complete"
                )
                
                # Get the page source and search for the test string using regex
                page_source = driver.page_source
                if re.search(test_string_pattern, page_source):
                    print(f"Test string found in the response for input: {element.get_attribute('outerHTML')}")
                else:
                    print(f"Test string NOT found in the response for input: {element.get_attribute('outerHTML')}")
                
                # Navigate back if needed to test the next input
                driver.back()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], textarea"))
            )

    driver.quit()

##########################################################################################################

def interact_and_check_response(url):
    test_string = "JLJL"
    test_string_pattern = r"JL.{0,26}JL"

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Scroll to the bottom of the page - be careful of infinite scroll websites here
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Find all input and textarea elements
    elements = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")

    # Filter elements that are displayed and enabled (interactable)
    interactable_elements = [e for e in elements if e.is_displayed() and e.is_enabled()]

    if not interactable_elements:
        print("""\nXX No interactable inputs found :(
              Note: Prone to false negatives - this script may not have done enough to make the inputs interactable.\n""")
    else:
        print(f"\n✓✓ {len(interactable_elements)} interactable input(s) found.\n")

    for element in elements:
        if element.is_displayed() and element.is_enabled():
            element.send_keys(test_string)  # Enter the test string

            # Attempt to find and click the associated submit button or image acting as a button
            try:
                form = element.find_element(By.XPATH, "./ancestor::form")
                # Look for input of type submit, button of type submit, or an img acting as a button
                submit_button = form.find_element(By.CSS_SELECTOR, "input[type=submit], button[type=submit], img[role=button], a.book--now, a.signup, a.submit, a.booknow")
                submit_button.click()

            except (NoSuchElementException, ElementNotInteractableException):
                print("No associated submit button or image acting as a button found for input")

            time.sleep(2)  # Adjust sleep time as needed

            # Check for an alert
            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert  # Switch to the alert
                print(f"✓✓ Alert found after submitting input: '{alert.text}'\n")
            except TimeoutException:
                print("XX No alert found after submitting input.")

            if not EC.alert_is_present:
            # Get the page source and search for the test string using regex
                page_source = driver.page_source
                if re.search(test_string_pattern, page_source):
                    print(f"✓✓ Test string found in the response for input.")
                else:
                    print(f"XX Test string NOT found in the response for input.")

                # Navigate back to test the next input
                driver.back()

    driver.quit()

##############################################################################################################

def load_search_strings(filename):
    
    """Helper function to load search strings from a file."""
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []

def static_analysis(url):
    # Map category names to filenames
    categories_files = {
        'Databases': 'databases.txt',
        'HTML comments': 'html_comments.txt',
        'HTML meta tags': 'html_meta_tags.txt',
        'HTML input tags': 'html_input_tags.txt',
        'JavaScript tags': 'javascript_tags.txt',
        'Front-end filtering': 'frontend_filtering.txt'
    }

    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    content_lines = response.text.splitlines()

    # Iterate over each category
    for category, filename in categories_files.items():
        search_strings = load_search_strings(filename)
        found = False  # Flag to track if any string is found
        
        print(f"""------------------------------------------------
              \n--> Searching for {category}...\n""")
        
        for line_number, line in enumerate(content_lines, 1):
            for string in search_strings:
                if string in line:                    
                    print(f"""      ✓✓ '{string}' mentioned on line {line_number}:{line.strip()}\n""")
                    found = True
        
        if not found:
                print(f"      XX No evidence of {category} found :(\n")

def banner_grab(url):
    # Parse the URL to extract the domain and possible port
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split(':')[0]  # Get the domain without the port
    port = parsed_url.port if parsed_url.port else 80  # Use port 80 if no port specified

    def send_request(request):
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)  # Set timeout for the socket
            # Connect to the server
            s.connect((domain, port))
            # Send the HTTP request to the server
            s.send(request.encode())
            # Receive the response from the server
            response = s.recv(4096)  # Adjust size as necessary
            s.close()  # Always close the socket
            # Decode and split the response at the first double newline, which ends the headers
            headers, _, _ = response.decode().partition('\r\n\r\n')
            return headers
        except Exception as e:
            return f"Failed to connect or retrieve data: {e}"
        

    # Standard HTTP GET request
    normal_request = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
    headers = send_request(normal_request)
    print(f"""
--> BANNER GRABBING {url}
================================================================================

> Normal GET request sent:\n{normal_request}
> Normal GET request response:\n{headers}
--------------------------------------------------------------------------------""")


    # Malformed GET request with non-existent method 'FAKE'
    malformed_request = f"GET / FAKE/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
    headers = send_request(malformed_request)
    print(f"""
> Malformed GET request sent with non-existent protocol 'FAKE':\n{malformed_request}
> Malformed GET request reponse:\n{headers}
--------------------------------------------------------------------------------""")


    # Malformed request with non-existent method 'FAKE'
    malformed_request = f"FAKE / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
    headers = send_request(malformed_request)
    print(f"""
> Malformed FAKE request sent with non-existent method 'FAKE':\n{malformed_request}
> Malformed FAKE request response:\n{headers}
--------------------------------------------------------------------------------""")
    
    # Different HTTP versions
    malformed_request = f"GET / HTTP/1.0\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
    headers = send_request(malformed_request)
    print(f"""
> HTTP version 1.0 request sent:\n{malformed_request}
> HTTP version 1.0 request response:\n{headers}
--------------------------------------------------------------------------------""")
    
    # Different HTTP versions
    malformed_request = f"GET / HTTP/2.0\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
    headers = send_request(malformed_request)
    print(f"""
> HTTP version 2.0 request sent:\n{malformed_request}
> HTTP version 2.0 request response:\n{headers}
--------------------------------------------------------------------------------""")
    
##############################################################################################################

# Get More Detailed DNS Information
def dns_lookup(url, record_type):
    try:
        # Perform the DNS query
        response = dns.resolver.resolve(url, record_type)
        
        # Print details about the DNS response
        print(f"Query for {url} {record_type} records:")
        for answer in response:
            print(f"  - {record_type} record: {answer.to_text()}")
            print(f"    TTL: {answer.ttl} seconds")
        
        # Print additional response information
        print("\nAdditional response metadata:")
        print(f"  Query time: {response.response.time * 1000:.2f} ms")
        print(f"  urlservers used for the query:")
        for ns in response.urlservers:
            print(f"    {ns}")
        
    except dns.resolver.NoAnswer:
        print(f"No {record_type} record found for {url}")
    except dns.resolver.NXDOMAIN:
        print(f"The domain {url} does not exist")
    except dns.resolver.Timeout:
        print("The request timed out")
    except Exception as e:
        print(f"Error: {e}")

####################################################################################################

def get_url(url):
    print("\n--> Trying to get IP address..\n")
    try:
        # Extract the hostname from the URL
        hostname = urlparse(url).hostname
        # Resolve the hostname to an IP address
        url = socket.gethostbyname(hostname)
        print(f"The IP address of {url} is {url}")
    except socket.error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#######################################################################################################