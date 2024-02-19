# COMP 348 Assignment 2

import requests
from bs4 import BeautifulSoup

print("***** Web Scraping Adventure *****")
print("1. Display Latest Deals")
print("2. Analyze Deals by Category")
print("3. Find Top Stores")
print("4. Log Deal Information")
print("5. Exit")
choice = input("Enter your choice (1-5): ")

while 1:
    if choice == "1":
        print("bleh")
    #elif choice == "2":
        
    #elif choice == "3":
        
    #elif choice == "4":
        
    elif choice == "5":
        exit()
        
    else:
        choice = input("Invalid input, please input a number between 1 and 5: ")