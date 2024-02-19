# COMP 348 Assignment 2

import requests
from bs4 import BeautifulSoup

def get_store(listing):
    """
    Extracts the store name from the given listing.

    Parameters:
    - listing (BeautifulSoup): The BeautifulSoup object representing a deal listing.

    Returns:
    - str: The extracted store name.
    """
    store_element_retailer = listing.select_one('.topictitle_retailer')
    store_element = listing.select_one('.topictitle')

    if store_element_retailer:
        return store_element_retailer.text.strip()
    elif store_element:
        # Extract store from the square brackets, if available
        store_text = store_element.text.strip()
        return store_text.split(']')[0][1:].strip() if ']' in store_text else store_text
    else:
        return "N/A"

print("***** Web Scraping Adventure *****")
print("1. Display Latest Deals")
print("2. Analyze Deals by Category")
print("3. Find Top Stores")
print("4. Log Deal Information")
print("5. Exit")
#choice = input("Enter your choice (1-5): ")

url = "https://forums.redflagdeals.com/"
response = requests.get(url + "hot-deals-f9/")
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

# Example: Extracting information from HTML elements
# Base URL
base_url = "https://forums.redflagdeals.com/"

for listing in soup.find_all("li", class_="row topic"):
    store = get_store(listing)

    item_element = listing.select_one('.topic_title_link')
    item = item_element.text.strip() if item_element else "N/A"

    # You may repeat the same for 
    # votes = ('.total_count_selector')
    # username=('.thread_meta_author')
    # timestamp =('.first-post-time')
    # category =('.thread_category a')
    # replies =('.posts')
    # views =('.views')
    
    # Extract the URL and prepend the base URL
    url_element = item_element['href'] if item_element else "N/A"
    url = base_url + url_element
    
    # You should store this info in a structured manner.
    # A simple print to show the data
    print(f"Store: {store}")
    print(f"Title: {item}")
    print(f"Url: {url}")
    print("-------------------------")

'''while 1:
    if choice == "1":
        
    #elif choice == "2":
        
    #elif choice == "3":
        
    #elif choice == "4":
        
    elif choice == "5":
        exit()
        
    else:
        choice = input("Invalid input, please input a number between 1 and 5: ")
'''