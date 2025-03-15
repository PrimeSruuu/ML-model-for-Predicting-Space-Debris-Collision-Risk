import requests
import psycopg2
from datetime import datetime

# Space-Track credentials
USERNAME = "useofonline@gmail.com"
PASSWORD = "susinginonlineeeee-25"

# PostgreSQL credentials
DB_NAME = "space_debris"
DB_USER = "postgres"
DB_PASSWORD = "DPRS"
DB_HOST = "localhost"
DB_PORT = "5432"

# Space-Track API URLs
SATELLITE_URL = "https://www.space-track.org/basicspacedata/query/class/tle_latest/OBJECT_TYPE/PAYLOAD/orderby/ORDINAL%20asc/emptyresult/show"
DEBRIS_URL = "https://www.space-track.org/basicspacedata/query/class/tle_latest/OBJECT_TYPE/DEBRIS/orderby/ORDINAL%20asc/limit/1000/emptyresult/show"

# Function to authenticate and fetch data
def fetch_data(url):
    session = requests.Session()
    login_url = "https://www.space-track.org/ajaxauth/login"
    login_data = {"identity": USERNAME, "password": PASSWORD}

    # Authenticate
    response = session.post(login_url, data=login_data)
    if response.status_code != 200:
        print("Login failed!")
        return []

    # Fetch data
    response = session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return []

# Function to insert data into PostgreSQL
def insert_data(data, table):
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()

    for obj in data:
        query = f"""
        INSERT INTO {table} (object_name, norad_id, epoch, mean_motion, eccentricity, inclination, 
        ra_of_asc_node, arg_of_pericenter, mean_anomaly, tle_line1, tle_line2, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (norad_id) DO UPDATE 
        SET epoch = EXCLUDED.epoch, mean_motion = EXCLUDED.mean_motion,
            eccentricity = EXCLUDED.eccentricity, inclination = EXCLUDED.inclination,
            ra_of_asc_node = EXCLUDED.ra_of_asc_node, arg_of_pericenter = EXCLUDED.arg_of_pericenter,
            mean_anomaly = EXCLUDED.mean_anomaly, tle_line1 = EXCLUDED.tle_line1,
            tle_line2 = EXCLUDED.tle_line2, last_updated = NOW();
        """
        values = (
            obj.get("OBJECT_NAME"),
            obj.get("NORAD_CAT_ID"),
            obj.get("EPOCH"),
            obj.get("MEAN_MOTION"),
            obj.get("ECCENTRICITY"),
            obj.get("INCLINATION"),
            obj.get("RA_OF_ASC_NODE"),
            obj.get("ARG_OF_PERICENTER"),
            obj.get("MEAN_ANOMALY"),
            obj.get("TLE_LINE1"),
            obj.get("TLE_LINE2"),
        )
        cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

# Fetch and store data
satellites = fetch_data(SATELLITE_URL)
debris = fetch_data(DEBRIS_URL)

insert_data(satellites, "satellites")
insert_data(debris, "debris")

print("Data successfully stored in PostgreSQL!")
