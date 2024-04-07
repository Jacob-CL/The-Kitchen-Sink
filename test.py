import re

# Define the regex pattern
pattern = r"JL.{0,26}JL"

# Test string
test_string = r"JLJL"

# Search for the pattern
match = re.search(pattern, test_string)

# Check if the pattern was found
if match:
    print("Match found:", match.group())
else:
    print("No match found.")
