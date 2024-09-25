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
meal_num = 0
for meal in meals:
    meal_num += 1
    cleaned_meal_name = re.sub(r'\s*\(\d{1,2}(:\d{2})?[ap]m-\d{1,2}(:\d{2})?[ap]m\)\s*', '', meal.text).strip()  # Cleans the meal name
    meal_start_time = re.search(r'\d{1,2}(:\d{2})?[ap]m', meal.text).group(0)  # Finds the start time of the meal
    meal_end_time = re.search(r'(?<=-)\d{1,2}(:\d{2})?[ap]m', meal.text).group(0)  # Finds the end time of the meal
    
    # Parse the start time string into a datetime object
    meal_start_time = datetime.strptime(meal_start_time, '%I:%M%p' if ':' in meal_start_time else '%I%p').time()
    meal_end_time = datetime.strptime(meal_end_time, '%I:%M%p' if ':' in meal_end_time else '%I%p').time()

    # Format the time as needed (e.g., 'HH:MM:SS')
    meal_start_time_formatted = meal_start_time.strftime('%H:%M:%S')
    meal_end_time_formatted = meal_end_time.strftime('%H:%M:%S')

    # Upsert the meal data into the Supabase Meal table
    try:
        response = (
            supabase.table("Meals")
            .upsert(
                {
                    "meal_name": cleaned_meal_name,
                    "meal_start_time": meal_start_time_formatted,
                    "meal_end_time": meal_end_time_formatted,
                    "meal_date": datetime.now().strftime('%Y-%m-%d'),
                },
                on_conflict=["meal_id", "meal_name", "meal_start_time", "meal_end_time", "meal_date"],  # Specifies column to check for conflicts
            )
            .execute()
        )
        # Retrieve the meal_id from the response
        meal_id = response.data[0]['meal_id']
    except Exception as message:
        print("Error upserting meal data: ", message)
    exit()

    current_meal = soup.find("div", {"id": "tabinfo-" + (str)(meal_num)})  # Finds the each meal of the day by its id

    stations = current_meal.find_all("div", {"class": "menu-station"})

    for station in stations:
        # Finds each menu item and its station name.
        station_name = station.find("button").text

        # Upsert the meal data into the Supabase FoodStation table
        try:
            response = (
                supabase.table("FoodStations")
                .upsert(
                    {
                        "station_name": station_name,
                        "meal_id": meal_id,
                    },
                    on_conflict=["station_id", "station_name", "meal_id"],  # Specifies column to check for conflicts
                )
                .execute()
            )
            # Retrieve the station_id from the response
            station_id = response.data[0]['station_id']
        except Exception as message:
            print("Error upserting food station data: ", message)
        
        items = station.find_all("li", {"class": "menu-item-li"})
        for item in items:
            item_name = item.find("a").text
            data = requests.get(item_url + item.find("a").get("data-recipe"))  # Get the recipe json data for the item using the id
            html = data.json().get("html", "")  # Parse the html from the json data
            item_soup = BeautifulSoup(html, "html.parser")
            p_tags = item_soup.find_all("p")
            ingredients = p_tags[len(p_tags) - 1].text.replace("Ingredients: ", "")
            # Upsert the meal data into the Supabase MealsOptions table
            try:
                response = (
                    supabase.table("MealsOptions")
                    .upsert(
                        {
                            "station_id": station_id,
                            "option_name": item_name,
                            "ingredients": ingredients,
                        },
                        on_conflict=["option_id", "station_id", "option_name", "ingredients"],  # Specifies column to check for conflicts
                    )
                    .execute()
                )
                # Retrieve the option_id from the response
                option_id = response.data[0]['option_id']
            except Exception as message:
                print("Error upserting food options data: ", message)
            # Finds item descriptions, however most items have no description
            # description = nutrition_soup.find("p").text.split("<\/p>")[0]
            try:
                allergens = item_soup.find("div", {"id": 'nutrition-info-header'}).find("p").text.split(",")  # Finds the allergens in a string seperated by commas
                for allergen in allergens:
                    # Upsert the meal data into the Supabase MealsOptions table
                    try:
                        response = (
                            supabase.table("NutrientInformation")
                            .upsert(
                                {
                                    "option_id": option_id,
                                    "nutrient_name": allergen,
                                    "nutrient_value": 1,
                                },
                                on_conflict=["nutrient_id", "option_id", "nutrient_name", "nutrient_value"],  # Specifies column to check for conflicts
                            )
                            .execute()
                        )
                    except Exception as message:
                        print("Error upserting allergen data: ", message)
            except:
                print("No allergens found")
            nutrition_entries = item_soup.find_all("tr")  # Finds the nutrition info in a table
            for nutrition_entry in nutrition_entries:
                nutrition_mapping = str.maketrans("", "", " \n\t")  # Specifies characters that should be removed from the found values
                nutrition_info = nutrition_entry.find("th").text.translate(nutrition_mapping)
                nutrition_info = re.split(r'(\d+|\D+|½)', nutrition_info, 1)  # Splits the string into two parts at the first digit (creates a list with 3 elements first is empty)
                # Upsert the meal data into the Supabase MealsOptions table
                try:
                    response = (
                        supabase.table("NutrientInformation")
                        .upsert(
                            {
                                "option_id": option_id,
                                "nutrient_name": nutrition_info[1],
                                "nutrient_value": nutrition_info[2],
                            },
                            on_conflict=["nutrient_id", "option_id", "nutrient_name", "nutrient_value"],  # Specifies column to check for conflicts
                        )
                        .execute()
                    )
                except Exception as message:
                    print("Error upserting nutrient data: ", message)