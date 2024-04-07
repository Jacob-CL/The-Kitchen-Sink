from selenium import webdriver
from selenium.webdriver.common.by import By

def count_interactable_inputs(url):
    # Setup WebDriver; make sure to specify the correct path to your WebDriver executable
    driver = webdriver.Firefox()
    
    # Open the specified URL
    driver.get(url)
    
    # Find all input and textarea elements
    elements = driver.find_elements(By.CSS_SELECTOR, "input, textarea")
    
    # Count elements that are displayed and enabled (interactable)
    interactable_count = sum(1 for element in elements if element.is_displayed() and element.is_enabled())
    
    # Close the browser window
    driver.quit()
    
    return interactable_count

# Specify the URL for Google's homepage
url = 'https://www.google.com'

# Print the number of interactable inputs
print(f"Number of interactable inputs on Google's homepage: {count_interactable_inputs(url)}")
