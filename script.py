import requests
import json
import boto3
from datetime import datetime, timedelta

def fetch_historical_weather(api_key, city, start_date, end_date):
    base_url = "http://api.openweathermap.org/data/2.5/onecall/timemachine"

    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    historical_data = []

    current_timestamp = start_timestamp
    while current_timestamp <= end_timestamp:
        response = make_api_request(base_url, api_key, city, current_timestamp)
        
        if response.status_code == 200:
            data = response.json()
            historical_data.append(data)
        else:
            print(f"Failed to fetch data for {datetime.utcfromtimestamp(current_timestamp)}")

        current_timestamp += 86400  # Move to the next day

    return historical_data

def make_api_request(base_url, api_key, city, timestamp):
    latitude, longitude = get_city_coordinates(city)
    url = f"{base_url}?lat={latitude}&lon={longitude}&dt={timestamp}&appid={api_key}"
    response = requests.get(url)
    return response

def get_city_coordinates(city):
    # Use a geocoding API to get the actual latitude and longitude based on the city name
    # Replace the following with actual geocoding logic
    return 19.0760, 72.8777  # Mumbai's approximate coordinates

def upload_to_s3(bucket_name, file_key, data):
    s3 = boto3.client('s3')

    # Convert data to JSON string
    data_json = json.dumps(data)

    # Upload to S3
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=data_json)

# ...

if __name__ == "__main__":
    api_key = '1152748302afb1a2fbff5b475a6e9a08'
    city = 'Mumbai'
    start_date = '2023-01-01'
    end_date = '2023-01-10'
    s3_bucket_name = 'forweatherdata8349'  # Replace with your S3 bucket name

    # Generate a dynamic file key based on the date range
    s3_file_key = f"historical_weather_data_{start_date}_to_{end_date}.json"

    historical_data = fetch_historical_weather(api_key, city, start_date, end_date)

    for data in historical_data:
        temperature = data.get('current', {}).get('temp')
        print(f"Temperature on {datetime.utcfromtimestamp(data['current']['dt'])}: {temperature} °C")

    # Upload data to S3
    upload_to_s3(s3_bucket_name, s3_file_key, historical_data)
    print(f"Data uploaded to S3: s3://{s3_bucket_name}/{s3_file_key}")
