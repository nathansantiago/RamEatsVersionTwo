#Scraper Imports
import requests, re, os
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)


#Scrape Data
location_url = "https://dining.unc.edu/locations/chase/"
item_url = "https://dining.unc.edu/wp-content/themes/nmc_dining/ajax-content/recipe.php?recipe="
data = requests.get(location_url)
html = data.text

soup = BeautifulSoup(html, "html.parser")

meals = soup.find_all("button", {"class": "c-tabs-nav__link"})  # Finds all the meal buttons on the page
for meal in meals:
    cleaned_meal_name = re.sub(r'\s*\(\d{1,2}[ap]m-\d{1,2}[ap]m\)\s*', '', meal.text).strip()  # Cleans the meal name
    meal_start_time = re.search(r'\d{1,2}[ap]m', meal.text).group(0)  # Finds the start time of the meal
    meal_end_time = re.search(r'(?<=-)\d{1,2}[ap]m', meal.text).group(0)  # Finds the end time of the meal
    
    # Parse the start time string into a datetime object
    meal_start_time = datetime.strptime(meal_start_time, '%I%p').time()
    meal_end_time = datetime.strptime(meal_end_time, '%I%p').time()

    # Format the time as needed (e.g., 'HH:MM:SS')
    meal_start_time_formatted = meal_start_time.strftime('%H:%M:%S')
    meal_end_time_formatted = meal_end_time.strftime('%H:%M:%S')

    # Upsert the meal data into the Supabase table
    try:
        response = (
            supabase.table("Meals")
            .upsert(
                {
                    "meal_id": hash(cleaned_meal_name),
                    "meal_name": cleaned_meal_name,
                    "meal_start_time": meal_start_time_formatted,
                    "meal_end_time": meal_end_time_formatted,
                },
                on_conflict=["meal_id", "meal_name", "meal_start_time", "meal_end_time"],  # Specifies column to check for conflicts
            )
            .execute()
        )
    except:
        print("Error upserting meal data: ", Exception)

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
        allergens = item_soup.find("div", {"id": 'nutrition-info-header'}).find("p").text  # Finds the allergens in a string seperated by commas
        nutrition_entries = item_soup.find_all("tr")  # Finds the nutrition info in a table
        for nutrion_entry in nutrition_entries:
            nutrition_mapping = str.maketrans("", "", " \n\t")  # Specifies characters that should be removed from the found values
            nutrition_info = nutrion_entry.find("th").text.translate(nutrition_mapping)
            nutrition_info = re.split(r'(\d+|\D+)', nutrition_info, 1)  # Splits the string into two parts at the first digit (creates a list with 3 elements first is empty)
            print(nutrition_info)
        exit()