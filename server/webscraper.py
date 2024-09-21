#Scraper Imports
import requests, json, re
from bs4 import BeautifulSoup

#Scrape Data
location_url = "https://dining.unc.edu/locations/chase/"
item_url = "https://dining.unc.edu/wp-content/themes/nmc_dining/ajax-content/recipe.php?recipe="
data = requests.get(location_url)
html = data.text

soup = BeautifulSoup(html, "html.parser")

meal = soup.find("div", {"id": "tabinfo-3"})  # Finds the third meal of the day manipulate the number for each meal

stations = meal.find_all("div", {"class": "menu-station"})

# Finds each menu item and its station name.
for station in stations:
    station_name = station.find("button").text
    # print(station_name)
    items = station.find_all("li", {"class": "menu-item-li"})
    for item in items:
        item_name = item.find("a").text
        data = requests.get(item_url + item.find("a").get("data-recipe"))  # Get the recipe json data for the item using the id
        html = data.json().get("html", "")  # Parse the html from the json data
        item_soup = BeautifulSoup(html, "html.parser")
        # Finds item descriptions, however most items have no description
        # description = nutrition_soup.find("p").text.split("<\/p>")[0]
        #  TODO: Parse the returned allergen string into a list of allergens
        allergens = item_soup.find("div", {"id": 'nutrition-info-header'}).find("p").text  # Finds the allergens in a string seperated by commas
        nutrition_entries = item_soup.find_all("tr")  # Finds the nutrition info in a table
        for nutrion_entry in nutrition_entries:
            nutrition_name = nutrion_entry.find("th").text.strip().replace(" ", "")
            print(nutrition_name)
        exit()