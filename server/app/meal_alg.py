from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from typing import List, Dict, Any
import os

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def calculate_meal(user_data: Dict[str, Any], menu: List[Dict[str, Any]]) -> Dict[str, Any]:
    maintenance_cal = user_data["maintainance_cal"]
    fitness_goal = user_data["fitness_goal"]
    user_data['height'] *= 2.54  # Convert height from inches to cm
    user_data['weight'] *= 0.453592  # Convert weight from lbs to kg
    # TODO: Calculate daily total calories based on user's fitness goal (how does the goal correspond to bulk, maintain, cut?)
    daily_tot_cal = maintenance_cal
    meal_cal = daily_tot_cal
    meal_cal_lower = meal_cal - 50
    meal_cal_upper = meal_cal + 50
    protein_goal = 0.24 * meal_cal_upper
    carbs_goal = 0.53 * meal_cal_upper
    fats_goal = 0.23 * meal_cal_upper

    selected_items = []
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0

    for info in menu:
        if total_calories + info["Calories"] <= meal_cal_upper:
            if ((total_protein + info["Protein"]) / meal_cal_upper) <= protein_goal \
                and ((total_carbs + info["TotalCarbohydrate"]) / meal_cal_upper) <= carbs_goal \
                and ((total_fats + info["TotalFat"]) / meal_cal_upper) <= fats_goal:

                remaining_calories = meal_cal_upper - total_calories
                portion = 1.0
                if info["Calories"] > remaining_calories:
                    portion = remaining_calories / info["Calories"]

                selected_items.append((info["Name"], portion))
                total_calories += info["Calories"] * portion
                total_protein += info["Protein"] * portion
                total_carbs += info["TotalCarbohydrate"] * portion
                total_fats += info["TotalFat"] * portion
        else:
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
