import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from meal_alg import calculate_meal
from utils.utils import get_menu_data, get_station_id, categorize_items, calculate_daily_cal


def test_get_station_id():
    station_name = "Simply Prepared Grill"
    station_id = get_station_id(station_name, "Lunch")
    assert station_id is not None, f"Station ID for {station_name} should not be None."
    print(f"Station ID for {station_name}: {station_id}")


def test_get_menu_data():
    station_id = get_station_id("Simply Prepared Grill", "Lunch")
    menu_data = get_menu_data(station_id)
    assert menu_data is not None, f"Menu data for station ID {station_id} should not be None."
    print(f"Menu data for station ID {station_id}: {menu_data}")

def test_categorize_items():
    station_id = get_station_id("Simply Prepared Grill", "Lunch")
    menu_data = get_menu_data(station_id)
    categorized_items = categorize_items(menu_data)
    assert categorized_items is not None, f"Categorized items for station ID {station_id} should not be None."
    print(f"Categorized items for station ID {station_id}: {categorized_items}")

def test_calculate_daily_cal():
    user_data = {
        "height": 67.0,
        "weight": 150.0,
        "age": 20,
        "activity_level": 20,
        "gender": False,
        "fitness_goal": 1,
        "meal_count": 3
    }
    daily_cal = calculate_daily_cal(user_data)
    assert daily_cal is not None, f"Daily caloric intake should not be None."
    print(f"Daily caloric intake: {daily_cal}")

def test_calculate_meal():
    user_data = {
        "height": 67.0,
        "weight": 150.0,
        "age": 20,
        "activity_level": 20,
        "gender": False,
        "fitness_goal": 1,
        "meal_count": 3
    }
    station_id = get_station_id("Simply Prepared Grill", "Lunch")
    menu_data = get_menu_data(station_id)
    categorized_items = categorize_items(menu_data)
    meal = calculate_meal(user_data, categorized_items)
    print(f"Meal: {meal}")


if __name__ == "__main__":
    test_calculate_meal()