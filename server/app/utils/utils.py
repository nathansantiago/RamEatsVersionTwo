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


def get_station_id(station_name: str) -> int:
    response = supabase.table('FoodStations').select("station_id").eq('station_name', station_name).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Station not found")
    return response.data[0]['station_id']


def get_menu_data(station: int) -> List[Dict[str, Any]]:
    response = supabase.table('MealOptions').select("*").eq('station_id', station).execute()
    return response.data


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