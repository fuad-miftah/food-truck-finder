import os
import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from math import sqrt
from datetime import datetime
from django.shortcuts import render

def home(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if not latitude or not longitude:
            return JsonResponse({"error": "Latitude and longitude are required"}, status=400)
        try:
            user_latitude = float(latitude)
            user_longitude = float(longitude)
        except ValueError:
            return JsonResponse({"error": "Invalid latitude or longitude"}, status=400)

        facility_type = request.POST.get('facility_type')
        results = int(request.POST.get('results', 10))
        food_items = request.POST.getlist('food_items[]') if request.POST.getlist('food_items[]') else []

        csv_file_path = os.path.join(settings.BASE_DIR, 'food-truck-data.csv')

        try:
            df = pd.read_csv(csv_file_path)
        except FileNotFoundError:
            return JsonResponse({"error": "CSV file not found"}, status=500)
        
        df = df[df['Status'] == 'APPROVED']

        try:
            df['ExpirationDate'] = pd.to_datetime(df['ExpirationDate'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
        except ValueError:
            return JsonResponse({"error": "Error converting date to datetime"}, status=500)

        df = df.dropna(subset=['ExpirationDate'])

        if facility_type and facility_type != 'All':
            df = df[df['FacilityType'] == facility_type]

        if food_items:
            df['FoodItems'] = df['FoodItems'].fillna('')
            food_items_lower = [item.lower() for item in food_items]
            df['FoodItems'] = df['FoodItems'].str.lower()
            mask = df['FoodItems'].str.contains('|'.join(food_items_lower))
            df = df[mask]

        def euclidean_distance(lat1, lon1, lat2, lon2):
            # Convert latitude and longitude from degrees to kilometers
            lat_km = (lat2 - lat1) * 111.32
            lon_km = (lon2 - lon1) * 111.32

            # Calculate Euclidean distance
            distance = sqrt(lat_km**2 + lon_km**2)
            return distance

        df['distance'] = df.apply(lambda x: euclidean_distance(user_latitude, user_longitude, x['Latitude'], x['Longitude']), axis=1)

        try:
            df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
        except ValueError:
            return JsonResponse({"error": "Error converting distance to numeric"}, status=500)

        today = datetime.today()
        df = df[df['ExpirationDate'] > today]

        closest_food_trucks = df.nsmallest(results, 'distance')

        data = [{
            'applicant': truck['Applicant'],
            'distance': truck['distance'],
            'locationDescription': truck['LocationDescription'],
            'address': truck['Address'],
            'facilityType': truck['FacilityType'],
            'foodItems': truck['FoodItems'],
            'expirationDate': truck['ExpirationDate'].strftime('%m/%d/%Y %I:%M:%S %p')  # Format date as string
        } for _, truck in closest_food_trucks.iterrows()]

        context = {
            'data': data
        }
        return render(request, 'results.html', context)

    else:
        csv_file_path = os.path.join(settings.BASE_DIR, 'food-truck-data.csv')
        try:
            df = pd.read_csv(csv_file_path)
            df = df[df['Status'] == 'APPROVED']
            facility_types = df['FacilityType'].unique()
            food_items = df['FoodItems'].str.split(':').explode().str.strip().unique()
        except FileNotFoundError:
            facility_types = []
            food_items = []

        facility_types = [f_type for f_type in facility_types if pd.notna(f_type)]
        food_items = [f_item for f_item in food_items if pd.notna(f_item)]

        food_items.sort()

        context = {
            'facility_types': facility_types,
            'food_items': food_items
        }
        return render(request, 'home.html', context)
