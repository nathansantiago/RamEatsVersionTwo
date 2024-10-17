import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from meal_alg import app
from utils.utils import get_menu_data, get_station_id, categorize_items

client = TestClient(app)


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


if __name__ == "__main__":
    test_categorize_items()