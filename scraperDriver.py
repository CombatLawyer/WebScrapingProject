# COMP 348 Assignment 2

import requests
import os
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

# Web scaping url
base_url = "https://forums.redflagdeals.com/"
response = requests.get(base_url + "hot-deals-f9/")
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

deals = []

# For each deal scaped, strip the relevant data if present
for listing in soup.find_all("li", class_="row topic"):
    store = get_store(listing)

    item_element = listing.select_one('.topic_title_link')
    item = item_element.text.strip() if item_element else "N/A"
    
    votes_element = listing.select_one('.total_count_selector')
    votes = votes_element.text.strip() if votes_element else "N/A"
    
    username_element = listing.select_one('.thread_meta_author')
    username = username_element.text.strip() if username_element else "N/A"
    
    timestamp_element = listing.select_one('.first-post-time')
    timestamp = timestamp_element.text.strip() if timestamp_element else "N/A"
    
    category_element = listing.select_one('.thread_category a')
    category = category_element.text.strip() if category_element else "N/A"
    
    replies_element = listing.select_one('.posts')
    replies = replies_element.text.strip() if replies_element else "N/A"
    
    views_element = listing.select_one('.views')
    views = views_element.text.strip() if views_element else "N/A"
    
    # Extract the URL and prepend the base URL
    url_element = item_element['href'] if item_element else "N/A"
    url = base_url + url_element
    
    # Store deal data as a library
    deal = {"Store": store, "Title": item, "Votes": votes, "Username": username, "Timestamp": timestamp, "Category": category, "Replies": replies, "Views": views, "URL": url}
    
    # Append to the list containing all deals
    deals.append(deal)

while 1:
    
    # Print menu to display options
    print("***** Web Scraping Adventure *****")
    print("1. Display Latest Deals")
    print("2. Analyze Deals by Category")
    print("3. Find Top Stores")
    print("4. Log Deal Information")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")
    
    # Display deals if 1 is selected
    if choice == "1":
        print(f"Total deals: {len(deals)}")
        print("-----------------------------------------")
        for x in deals:
            # Printing Extracted data
            print(f"Store: {x['Store']}")
            print(f"Title: {x['Title']}")
            print(f"Votes: {x['Votes']}")
            print(f"Username: {x['Username']}")
            print(f"Timestamp: {x['Timestamp']}")
            print(f"Category: {x['Category']}")
            print(f"Replies: {x['Replies']}")
            print(f"Views: {x['Views']}")
            print(f"URL: {x['URL']}")
            print("-----------------------------------------")
    
    # Display all the categories and the number of deals for each
    elif choice == "2":
        
        # Get all categories
        allCategories = list(set(x['Category'] for x in deals))
        print("\nDeals by category:\n")
        dealsPerCategory = []
        
        # These variables are to allow the text on output to be justified to the longest category and the longest number of deals
        longestCategory = -1
        longestDeals = -1
        
        # For each category of deals count the number of deals which are under that specific category and keep track of the longest strings
        for dealCategory in allCategories:
            numDeals = len([x for x in deals if (x['Category'] == dealCategory)])
            dealsPerCategory.append((dealCategory, numDeals))
            longestCategory = len(dealCategory) if len(dealCategory) > longestCategory else longestCategory
            longestDeals = len(str(numDeals)) if len(str(numDeals)) > longestDeals else longestDeals
        
        # Sort by most deals and print the requested information    
        dealsPerCategory.sort(key=lambda x: x[1], reverse=True)
        for x in dealsPerCategory:
            print(x[0].rjust(longestCategory) + ": " + str(x[1]).ljust(longestDeals) +  " deals")
        print("-----------------------------------------")
        
    # Display the number of deals per store     
    elif choice == "3":
        
        # Get all stores
        allStores = list(set(x['Store'] for x in deals))
        
        # Get the number of stores to display, ensure that the input is within the correct range
        numStores = int(input(f"Enter the number of top stores to display (1-{len(allStores)}): "))
        while numStores < 1 or numStores > len(allStores):
            print(f"Error: Please use an input in the correct range (1-{len(allStores)}).")
            numStores = int(input(f"Enter the number of top stores to display (1-{len(allStores)}): "))
        dealsPerStore = []
        
        # Same variables to keep track of the longest string for both store name and number of deals
        longestStore = -1
        longestDeals = -1
        
        # For each store count the number of deals it has attached, while keeping track of the longest strings
        for dealStore in allStores:
            numDeals = len([x for x in deals if (x['Store'] == dealStore)])
            dealsPerStore.append((dealStore, numDeals))
            longestStore = len(dealStore) if len(dealStore) > longestStore else longestStore
            longestDeals = len(str(numDeals)) if len(str(numDeals)) > longestDeals else longestDeals
        
        # Sort by most deals and print the requested information
        dealsPerStore.sort(key=lambda x: x[1], reverse=True)
        for x in dealsPerStore[:numStores]:
            print(x[0].rjust(longestStore) + ": " + str(x[1]).ljust(longestDeals) +  " deals")
        print("-----------------------------------------")

    # Write to log deals of the specified category
    elif choice == "4":
        print("\nList of Categories\n")
        
        # Get all the categories and sort them alphabetically, these are then listed in a dictionary with their index
        allCategories = list(set(x['Category'] for x in deals))
        allCategories.sort()
        categorySelect = {}
        for i in range(1, len(allCategories) + 1):
            categorySelect[i] = allCategories[i-1]
            
        # Print the menu using the indexes in the dictionary
        for key, value in categorySelect.items():
            print(f"{key}. {value}")
        
        # Select the category to print deals, ensure the input is within the correct range
        numCategory = int(input("Enter the number corresponding to the category of interest: "))
        while numCategory < 1 or numCategory > len(allCategories):
            print(f"Error: Please use an input in the correct range (1-{len(allCategories)}).")
            for key, value in categorySelect.items():
                print(f"{key}. {value}")
            numCategory = int(input(f"Enter the number of top stores to display (1-{len(allCategories)}): "))
        
        # If the log file exists, rewrite it, otherwise create the file
        if not os.path.exists("log.txt"):
            file = open("log.txt", "x")
        else:
            file = open("log.txt", "w")
        
        # For the selected category, find deals from it and print the details to file
        categoryDeals = [x for x in deals if (x['Category'] == categorySelect[numCategory])]
        print(f"Recent deals in {categorySelect[numCategory]}", file=file)
        print(f"Total deals: {len(categoryDeals)}", file=file)
        print("-----------------------------------------", file=file)
        for x in categoryDeals:
            
            # Printing Extracted data
            print(f"Store: {x['Store']}", file=file)
            print(f"Title: {x['Title']}", file=file)
            print(f"Votes: {x['Votes']}", file=file)
            print(f"Username: {x['Username']}", file=file)
            print(f"Timestamp: {x['Timestamp']}", file=file)
            print(f"Category: {x['Category']}", file=file)
            print(f"Replies: {x['Replies']}", file=file)
            print(f"Views: {x['Views']}", file=file)
            print(f"URL: {x['URL']}", file=file)
            print("-----------------------------------------", file=file)
        file.close()
        print("All the links have been logged successfully.")
    elif choice == "5":
        print("Terminating program. Have a nice day!")
        exit()
        
    # This means that an invalid input was entered, print error message and print the main menu again       
    else:
        choice = input("Error, please enter a valid choice.")
