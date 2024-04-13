import socket
from urllib.parse import urlparse

# https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/01-Information_Gathering/02-Fingerprint_Web_Server

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
    print("--------------------------------------------------------------------------")
    print(f"Normal GET request sent: \n{normal_request}")
    print(f"Headers received: \n{headers}\n")

    # Malformed GET request with non-existent method 'FAKE'
    malformed_request = f"GET / FAKE/1.1\r\nHost: {domain}\r\nFake: Yes\r\nConnection: close\r\n\r\n"
    headers = send_request(malformed_request)
    print("--------------------------------------------------------------------------")
    print(f"Malformed GET request sent with non-existent protocol 'FAKE': \n{malformed_request}")
    print(f"Headers received: \n{headers}\n")

    # Malformed request with non-existent method 'FAKE'
    malformed_request = f"FAKE / HTTP/1.1\r\nHost: {domain}\r\nFake: Yes\r\nConnection: close\r\n\r\n"
    headers = send_request(malformed_request)
    print("--------------------------------------------------------------------------")
    print(f"Malformed GET request sent with non-existent method 'FAKE': \n{malformed_request}")
    print(f"Headers received: \n{headers}\n")  