import socket
from urllib.parse import urlparse

# https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/01-Information_Gathering/02-Fingerprint_Web_Server

def make_file():
    # Create a blank HTML file
    with open('InfoGathering.html', 'w') as file:
        file.write("""<!DOCTYPE html>
            <html>
            <head>
            <title>Information Gathering Report</title>
            </head>
            <body>
            <h1>Information Gathering Report</h1>
            <h1>========================================================================================</h1>""")

def close_file():
    with open('InfoGathering.html', 'a') as file:
        file.write("<br></body></html>")


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
        
    print("\n--> Banner Grabbing..")
    
    with open('InfoGathering.html', 'a') as file:
        # Standard HTTP GET request
        normal_request = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
        headers = send_request(normal_request)
        file.write(f"""
            <h2>Banner Grabbing</h2>
            <p>Normal GET request sent: <br><ul><li>{normal_request}</li></ul></p>
            <p>Normal GET request response: <br><ul><li>{headers}</li></ul></p><br>""")


        # Malformed GET request with non-existent method 'FAKE'
        malformed_request = f"GET / FAKE/1.1\r\nHost: {domain}\r\nFake: Yes\r\nConnection: close\r\n\r\n"
        headers = send_request(malformed_request)
        file.write(f"""
            <h1><strong>--------------------------------------------------------------------------</strong></h1>
            <p>Malformed GET request sent with non-existent protocol 'FAKE': <br><ul><li>{malformed_request}</li></ul></p>
            <p>Malformed GET request reponse: <br><ul><li>{headers}</li></ul></p><br>""")


        # Malformed request with non-existent method 'FAKE'
        malformed_request = f"FAKE / HTTP/1.1\r\nHost: {domain}\r\nFake: Yes\r\nConnection: close\r\n\r\n"
        headers = send_request(malformed_request)
        file.write(f"""
            <h1><strong>--------------------------------------------------------------------------</strong></h1>
            <p>Malformed FAKE request sent with non-existent method 'FAKE': <br><ul><li>{malformed_request}</li></ul></p>
            <p>Malformed FAKE request response: <br><ul><li>{headers}</li></ul></p><br>""")


def testfunction(file):
    with open('InfoGathering.html', 'a') as file:
        file.write("<h1>Please Print me</h1>")