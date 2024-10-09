from fastapi.responses import JSONResponse
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