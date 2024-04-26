import os
import re
import time
import socket
import requests
from urllib.parse import urlparse, urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

import dns.resolver

#########################################################################################################

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

def directorywalk(global_root_domain, paths_file):
    print("\n--> Enumerating URL by checking for all response codes less than 400...\n")

    # Open the file containing the paths
    with open(paths_file, 'r') as file:
        paths = file.read().splitlines()

    valid_urls = []
    # Iterate over the paths from the file and check each one
    for path in paths:
        # Construct the full URL
        url = urljoin(global_root_domain, path)

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
    
    print(f"\n✓✓ Directory walk enumeration on {global_root_domain} complete. \n")

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
    print("\n--> Grepping..\n")
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
    print(f"--> Counting number of interactable inputs in URL..")

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
    print(f"\n--> Starting static source code analysis..")
    # Map category names to filenames
    categories_files = {
        'Databases': 'databases.txt',
        'HTML comments': 'html_comments.txt',
        'HTML meta tags': 'html_meta_tags.txt',
        'HTML input tags': 'html_input_tags.txt',
        'JavaScript tags': 'javascript_tags.txt',
        'Front-end filtering': 'frontend_filtering.txt',
        'JavaScript Sources': 'sources.txt'
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
    
    print("\nFinished static analysis ✓✓\n")

#######################################################################################################################

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

def reverse_dns_lookup(ip_address):
    try:
        host, _, _ = socket.gethostbyaddr(ip_address)
        return host
    except socket.herror:
        return None

##############################################################################################################

def dns_lookup(input):
    # Check if input is an IP address and perform reverse DNS lookup if true
    try:
        # If this passes, input is an IP address
        socket.inet_aton(input)
        domain = reverse_dns_lookup(input)
        if domain is None:  # reverse lookup provided no new information
            print("Input is an IP address without DNS reverse records.")
            return
    except socket.error:
        # input is not an IP address, assume it's a domain
        domain = input

    record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS']
    for record_type in record_types:
        try:
            response = dns.resolver.resolve(domain, record_type)
            print(f"\nQuery for {domain} {record_type} records:")
            for answer in response:
                print(f"  - {record_type} record: {answer.to_text()}")
                print(f"    TTL: {answer.rrset.ttl} seconds")  # Access TTL through rrset
        except Exception as e:
            print(f"Failed to retrieve {record_type} records for {domain}: {e}")

####################################################################################################

def get_ip(url):
    print("\n--> Trying to get IP address..\n")
    try:
        # Extract the hostname from the URL
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if hostname is None:
            raise ValueError("URL does not contain a valid hostname - Make sure you have HTTP/HTTPS")

        # Resolve the hostname to an IP address
        ip = socket.gethostbyname(hostname)
        print(f"The IP address of {url} is {ip}")

    except socket.error as err:

        print(f"Error resolving hostname to IP: {err}")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#######################################################################################################

# SCAN COMMON PORTS
def common_port_scan(url):
    print(f"\n--> Scanning common ports..")
    # Create an Nmap PortScanner object
    nm = nmap.PortScanner()

    # List of common ports to scan
    common_ports = [
        '21',    # FTP
        '22',    # SSH
        '23',    # Telnet
        '25',    # SMTP
        '53',    # DNS
        '80',    # HTTP
        '110',   # POP3
        '143',   # IMAP
        '443',   # HTTPS
        '1433',  # MSSQL
        '3306',  # MySQL
        '3389',  # RDP
        '8080',   # HTTP alternative
        '40857'
    ]

    try:
        print("--> Performing NMAP scan on common ports with verbose output, returning only open ports..\n")
        # Convert the list of common ports into a comma-separated string for Nmap
        ports = ','.join(common_ports)
        # Run the scan with service and version detection
        nm.scan(url, ports, arguments='-sV -O')  # Including service detection and OS detection

        if nm.all_hosts():  # Check if any hosts were found
            for host in nm.all_hosts():  # Loop through all hosts
                print(f'Host : {host}')  # directly using `host` variable
                print(f'State : {nm[host].state()}')

                # Loop through all scanned protocols and corresponding ports
                for proto in nm[host].all_protocols():
                    print('----------')
                    print(f'Protocol : {proto}')

                    lport = nm[host][proto].keys()
                    for port in sorted(lport):
                        port_info = nm[host][proto][port]
                        # Print detailed information for each port
                        if port_info["state"] == "open":
                            print(f'Port : {port}\tState : {port_info["state"]}')
                            if 'url' in port_info:
                                print(f'\tService : {port_info["url"]}')
                            if 'product' in port_info:
                                print(f'\tProduct : {port_info["product"]}')
                            if 'version' in port_info:
                                print(f'\tVersion : {port_info["version"]}')
                            if 'extrainfo' in port_info:
                                print(f'\tExtra Info : {port_info["extrainfo"]}')
                            if 'script' in port_info:
                                print(f'\tScripts : {port_info["script"]}')
        else:
            print("No hosts found. Ensure the IP address or hosturl is correctly specified.")
    except Exception as error:
        print(f"Scan error: {error}")

#################################################################################################################

def port_scan_1024(url):
    nm = nmap.PortScanner()
    print("\n--> Quick scanning the first 1024 ports..\n")
    try:
        # Run a simple Nmap scan
        nm.scan(url, '1-1024')  # Scans TCP ports 1 through 1024
        if nm.all_hosts():  # Check if any hosts were found
            for host in nm.all_hosts():  # Loop through all hosts
                print('Host : %s (%s)' % (host, nm[host].hostname()))  # Get the host and its hostname
                print('State : %s' % nm[host].state())  # Get the state of the host (up/down)

                # Loop through all scanned protocols and corresponding ports
                for proto in nm[host].all_protocols():
                    print('----------')
                    print('Protocol : %s' % proto)

                    lport = nm[host][proto].keys()
                    for port in sorted(lport):
                        # Print port and state
                        print('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
        else:
            print("No hosts found. Make sure you've given it just an IP address - No HTTP or :portnumber")
    except Exception as error:
        print(f"""Scan error: {error}
Make sure you've given it just an IP address - No HTTP or :portnumber""")

###############################################################################################################

def search_strings_in_page(source, patterns):
    found_patterns = []
    for pattern in patterns:
        if re.search(pattern, source):
            found_patterns.append(pattern)
    return found_patterns

def find_sources(url):
    print(f"--> Dynamically checking for evidence of Javascript sources in URL: {url}")

    # Read patterns from the file named 'sources.txt'
    with open('sources.txt', 'r') as file:
        patterns = [line.strip() for line in file.readlines()]

    options = Options()
    options.headless = True  # Set to True if you don't want to see the browser window
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Scroll to the bottom of the page - be careful of infinite scroll websites here
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait to ensure the page has loaded completely

    # Get the page source after scrolling
    page_source = driver.page_source
    # Search the page source for each pattern from 'sources.txt'
    found_patterns = search_strings_in_page(page_source, patterns)
    if found_patterns:
        print(f"Source found: {found_patterns}")
    else:
        print("No sources patterns from 'sources.txt' were found.")

    driver.quit()

#########################################################################################################################