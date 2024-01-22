import requests
import json
from datetime import datetime, timedelta
import math
import random

# API endpoint
api_url = "http://10.8.0.4:8445/insert-water"

# Generate dataset for a week (7 days)
start_date = datetime.now()
end_date = start_date + timedelta(days=7)

current_date = start_date
while current_date < end_date:
    # Generate consumption values with highly realistic daily patterns
    for minute_offset in range(24 * 60 // 5):  # 24 hours in a day, 60 minutes in an hour, divided by 5 minutes interval
        hour = current_date.hour + minute_offset * 5 // 60
        weekday = current_date.weekday()  # 0 represents Monday, 6 represents Sunday

        # Determine if it's a weekday or weekend
        is_weekend = weekday >= 5

        # Determine if people are awake and active
        is_active = (7 <= hour <= 9 or 18 <= hour <= 20) and not (is_weekend and 10 <= hour <= 18)

        # Apply realistic consumption patterns
        base_consumption = 1.2
        if is_active:
            consumption_factor = base_consumption
            if 7 <= hour <= 9:  # Morning peak hours
                consumption_factor += 0.7
            elif 18 <= hour <= 20:  # Evening peak hours
                consumption_factor += 0.5

            # Introduce peak linked to showering
            if 6 <= hour <= 9:  # Morning shower peak
                consumption_factor += max(0, random.uniform(0.8, 1.2))
            elif 18 <= hour <= 20:  # Evening shower peak
                consumption_factor += max(0, random.uniform(0.6, 1.0))

            # Introduce peak linked to cooking
            if 17 <= hour <= 19:  # Cooking peak
                consumption_factor += max(0, random.uniform(0.5, 0.8))

        else:
            consumption_factor = 0  # Set consumption to zero during inactive periods

        # Introduce random events (e.g., guests, cleaning, gardening)
        random_event_chance = 0.02  # 2% chance of a random event
        random_event_value = max(0, random.uniform(0.5, 1.5))
        consumption_factor += random_event_value if random.random() < random_event_chance else 0

        # Seasonal variations
        seasonal_variation = 0.1 * math.sin(2 * math.pi * current_date.timetuple().tm_yday / 365)
        consumption_factor += seasonal_variation

        random_variation = random.uniform(-0.1, 0.1)  # Random variation

        consumption = max(0, round(base_consumption * consumption_factor + random_variation, 2))  # Adjust the range and factors
        data = {"conso": str(consumption)}

        # Make API call to insert data into the database
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            print(f"Data inserted successfully for {current_date} - Consumption: {consumption}")
            current_date += timedelta(minutes=5)
        else:
            print(f"Failed to insert data for {current_date} - Status Code: {response.status_code}")

    # Increment current date by 5 minutes
   # current_date += timedelta(days=1)

# Print a message when the script is done
print("Dataset generation completed.")
