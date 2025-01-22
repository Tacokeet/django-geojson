import requests
import geopandas as gpd

API_URL = "http://localhost:8000/features/"
DATASET = "municipalities_nl.geojson"
AUTH_URL = "http://localhost:8000/token/"

USERNAME = "admin"
PASSWORD = "admin"


def get_jwt_token() -> str:
    try:
        response = requests.post(AUTH_URL, json={
            "username": USERNAME,
            "password": PASSWORD
        })
        return response.json()["access"]
    except requests.exceptions.RequestException as e:
        print(f"Authentication failed: {e}")


def load_data():
    try:
        token = get_jwt_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        gdf = gpd.read_file(DATASET)
        for _, row in gdf.iterrows():
            data = {
                "name": row["name"],
                "geometry": row["geometry"].__geo_interface__,
            }
            response = requests.post(API_URL, json=data, headers=headers)
            print(response.status_code, response.json())
    
    except requests.exceptions.RequestException as e:
        print(f"Error during data loading: {e}")

if __name__ == "__main__":
    load_data()
