import os
import boto3
import requests
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['weatherfc']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        weather_data = fetch_weather_data()
        save_to_dynamodb(weather_data)
        return {'statusCode': 200, 'body': 'Data successfully updated in DynamoDB.'}
    except Exception as e:
        print('Error:', e)
        return {'statusCode': 500, 'body': 'Internal Server Error'}

def fetch_weather_data():
    api_key = os.environ['1152748302afb1a2fbff5b475a6e9a08']
    city = os.environ['MUMBAI']
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(api_url)
    response.raise_for_status()  # Raise an HTTPError for bad responses.

    return response.json()

def save_to_dynamodb(weather_data):
    timestamp = int(datetime.now().timestamp())

    params = {
        'TableName': table_name,
        'Item': {
            'timestamp': timestamp,
            'temperature': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity'],
            # Add other attributes as needed
        },
    }

    table.put_item(Item=params['Item'])
