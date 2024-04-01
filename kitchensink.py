import requests
from urllib.parse import urljoin
import validators
import logging
import os
import re
from banner import banner
import functions

print(banner())

option = input("""
Select an option:
    0. Throw the kitchen sink - walks through each option below, you choose which to execute
    1. Enumerate root URL and give me response codes
    2. Enumerate root URL and save valid URL's page source locally
    3. Find HTML input tags in page source
    4. Find and print comments in page source
    5. Find inline JavaScript <script> tags
    6. Look for evidence of XSS filters

""")

# The Kitchen sink:
if option == "0":
    url = input("""What URL are we throwing the kitchen sink at?
""")
    q1 = input("""Would you like to enumerate the URL and see the response codes? Y / N
""")
    if q1 == "Y" or q1 == "y":
        functions.enumerate_root_domain(url, 'paths.txt')

    q2 = input ("""Would you like to enumerate the URL and save valid URL's page source locally? Y / N
""")
    if q2 == "Y" or q2 == "y":
        functions.enumerate_and_save(url, 'paths.txt')

    q3 = input ("""Would you like to find HTML input tags? Y / N
""")
    if q3 == "Y" or q3 == "y":
        functions.search_for_HTML_input(url)

    q4 = input ("""Would you like to find HTML comments? Y / N
""")
    if q4 == "Y" or q4 == "y":
        functions.search_for_HTML_comments(url)   
    
    q5 = input ("""Would you like to search for inline JavaScript <script> tags? Y / N
""")
    if q5 == "Y" or q5 == "y":
        functions.search_for_javascript_tags(url)

    q6 = input("""Would you like to search for frontend XSS filtering?
""")
    if q6 == "Y" or q6 == 'y':
        functions.search_for_frontend_filtering(url)




if option == "1":
    #print(f"\nYou've selected to enumerate a root URL\n")
    url = input("What is the root URL of the page? Include 'https://www.'")
    functions.enumerate_root_domain(url, 'paths.txt')

if option == "2":
    #print(f"\nYou've selected to look for points of interest in the page sources\n")
    url = input("""
What is the root URL of the page? Include 'https://www.'
""")
    functions.enumerate_and_save(url, 'paths.txt')
    
if option == "3":
    #print(f"\nYou've selected to find HTML input tags\n")
    url = input("""
What is the URL of the page? Include 'https://www.'
""")
    functions.search_for_HTML_input(url)

if option == "4":
    #print(f"\nYou've selected find and print comments in page source\n")
    url = input("""
What is the URL of the page? Include 'https://www.'
""")
    functions.search_for_HTML_comments(url)

if option == "5":
    url = input("""
What is the URL of the page? Include 'https://www.'
""")
    functions.search_for_javascript_tags(url)

if option == "6":
    url = input("""
What is the URL of the page? Include 'https://www.'
""")
    functions.search_for_frontend_filtering(url)