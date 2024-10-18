from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from typing import List, Dict, Any
from dotenv import load_dotenv
from server.app.utils.utils import get_user_data, get_station_id, get_menu_data, categorize_items, calculate_daily_cal
import os
import re

app = FastAPI()
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def calculate_meal(user_data: Dict[str, Any], menu: List[Dict[str, Any]]) -> Dict[str, Any]:
    daily_cal = calculate_daily_cal(user_data)
    meal_cal = daily_cal // (user_data['meal_count'])
    meal_cal_lower = meal_cal - 50
    meal_cal_upper = meal_cal + 50
    protein_goal = 0.25 * meal_cal_upper  # Slightly reduced protein percentage
    carbs_goal = 0.50 * meal_cal_upper  # Adjusted carbohydrate percentage
    fats_goal = 0.25 * meal_cal_upper

    selected_items = {}
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0

    def convert_to_float(value: Any) -> float:
        if isinstance(value, float):
            return value
        elif isinstance(value, str):
            numeric_value = re.findall(r"[-+]?\d*\.\d+|\d+", value)
            return float(numeric_value[0]) if numeric_value else 0.0
        else:
            return 0.0

    # Sort menu items by protein content in descending order
    menu = sorted(menu, key=lambda x: convert_to_float(x.get("Protein", "0")), reverse=True)

    while total_calories < meal_cal_lower:
        for item in menu:
            info = {
                "Calories": convert_to_float(item.get("Calories", "0")),
                "Protein": convert_to_float(item.get("Protein", "0")),
                "TotalCarbohydrate": convert_to_float(item.get("TotalCarbohydrate", "0")),
                "TotalFat": convert_to_float(item.get("TotalFat", "0"))
            }

            if (total_calories + info["Calories"]) <= meal_cal_upper \
                and (total_protein + info["Protein"]) <= protein_goal \
                and (total_carbs + info["TotalCarbohydrate"]) <= carbs_goal \
                and (total_fats + info["TotalFat"]) <= fats_goal:
                if item["option_name"] not in selected_items:
                    selected_items[item["option_name"]] = {"number_of_servings": 1}
                else:
                    selected_items[item["option_name"]]["number_of_servings"] += 1

                total_calories += info["Calories"]
                total_protein += info["Protein"]
                total_carbs += info["TotalCarbohydrate"]
                total_fats += info["TotalFat"]

                # Break the loop if we are within the target range
                if total_calories >= meal_cal_lower:
                    break

    return {
        "selected_items": selected_items,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fats": total_fats
    }


@app.get("/recommend_meals")
async def recommend_meals(user_id: str):
    user_data = get_user_data(user_id)
    simply_prepared_station_id = get_station_id("Simply Prepared Grill")
    kitchen_table_station_id = get_station_id("Kitchen Table")

    simply_prepared_menu = get_menu_data(simply_prepared_station_id)
    kitchen_table_menu = get_menu_data(kitchen_table_station_id)

    categorized_simply_prepared = categorize_items(simply_prepared_menu)
    categorized_kitchen_table = categorize_items(kitchen_table_menu)

    simply_prepared_meal = calculate_meal(user_data, categorized_simply_prepared)
    kitchen_table_meal = calculate_meal(user_data, categorized_kitchen_table)

    return JSONResponse(content={
        "simply_prepared_meal": simply_prepared_meal,
        "kitchen_table_meal": kitchen_table_meal
    })