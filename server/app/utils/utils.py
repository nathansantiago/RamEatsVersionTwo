from fastapi import HTTPException
from supabase import create_client, Client
from typing import List, Dict, Any
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_user_data(user_uid: str) -> Dict[str, Any]:
    response = supabase.table('Users').select("*").eq('user_uid', user_uid).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]


def get_station_id(station_name: str, meal_time: str) -> int:
    response = (
        supabase.table('FoodStations')
        .select("station_id, meal_id")
        .eq("station_name", station_name)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Station not found")

    meal_id = get_meal_id(meal_time)
    station = next((record for record in response.data if record['meal_id'] == meal_id), None)

    if not station:
        raise HTTPException(status_code=404, detail=f"Station for {meal_time} not found")

    return station['station_id']


def get_meal_id(meal_time: str) -> int:
    meal_response = supabase.table('Meals').select("meal_id").eq("meal_name", meal_time).execute()
    if not meal_response.data:
        raise HTTPException(status_code=404, detail="Meal not found")

    return meal_response.data[0]['meal_id']


def get_menu_data(station: int) -> List[Dict[str, Any]]:
    menu_response = supabase.table('MealsOptions').select("*").eq('station_id', station).execute()
    menu_data = menu_response.data

    option_ids = [item['option_id'] for item in menu_data]
    nutrient_response = supabase.table('NutrientInformation').select(
        "option_id, nutrient_name, nutrient_value"
    ).in_("option_id", option_ids).execute()
    nutrient_data = nutrient_response.data

    nutrient_dict = {}
    for item in nutrient_data:
        option_id = item['option_id']
        if option_id not in nutrient_dict:
            nutrient_dict[option_id] = {}
        nutrient_dict[option_id][item['nutrient_name']] = item['nutrient_value']

    filtered_menu_data = [
        {key: value for key, value in item.items() if key != 'ingredients'} for item in menu_data
    ]

    merged_menu_data = []
    for item in filtered_menu_data:
        option_id = item['option_id']
        if option_id in nutrient_dict:
            merged_item = {**item, **nutrient_dict[option_id]}
            merged_menu_data.append(merged_item)

    return merged_menu_data


def categorize_items(menu: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Categorize items based on healthiness rating
    categorized_menu = sorted(menu, key=lambda x: (x["Protein"], -x["TotalFat"], -x["Sugar"]))
    return categorized_menu

def calculate_daily_cal(user_data: Dict[str, Any]) -> int:
    # Calculate BMR using Mifflin-St Jeor Equation
    user_data['height'] *= 2.54  # Convert height from inches to cm
    user_data['weight'] *= 0.453592  # Convert weight from lbs to kg
    pal = user_data['activity_level'] / 10

    if user_data['gender'] == False:
        # Calculate BMR for males
        bmr = 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age'] + 5
    else:
        # Calculate BMR for females
        bmr = 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age'] - 161
    
    # Calculate maintenance calories using BMR and activity level
    maintenance_cal = round(bmr * pal)

    if user_data['fitness_goal'] == 0:
        # Calculate daily caloric intake for bulking
        daily_tot_cal = round(maintenance_cal * 1.11)
    elif user_data['fitness_goal'] == 2:
        # Calculate daily caloric intake for cutting
        daily_tot_cal = round(maintenance_cal * 0.89)
    else:
        # Daily calories for maintaining weight
        daily_tot_cal = maintenance_cal

    return daily_tot_cal