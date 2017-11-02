# Import the urlopen function. We need this to read in the HTML
from urllib.request import urlopen, HTTPHandler

# Set a URL that we'll try to grab some HTML from.
url = "http://bobdylan.com/songs-played-live/"


# Open the URL and read the HTML content into a string variable
html_page = urlopen(url)
html_text = html_page.read()

# Print html_test string
print(html_text)