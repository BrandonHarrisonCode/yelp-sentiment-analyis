from flask import Flask, request, render_template, abort, url_for
from flask_dynamo import Dynamo
import boto3
import json
from decimal import Decimal
from boto3.session import Session
import geopy.distance

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Reviews')

app = Flask(__name__)


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    radius = float(request.args.get('radius')) / 1609
    if radius > 300:
        abort(400)
    
    restaurants = table.scan()['Items']
    print(restaurants)
    res = []
    for restaurant in restaurants:
        name = restaurant['Name']
        loc_lat = restaurant['Lat']
        loc_lng = restaurant['Lng']
        distance = geopy.distance.distance(
            (latitude, longitude), (loc_lat, loc_lng)).miles
        if distance <= radius:
            restaurant['Lat'] = float(restaurant['Lat'])
            restaurant['Lng'] = float(restaurant['Lng'])
            res.append(restaurant)
    return json.dumps(res)


@app.route('/dishes', methods=['GET'])
def get_dishes():
    restaurant_id = request.args.get('id')
    restaurant = table.get_item(Key={'RestaurantId': restaurant_id})['Item']

    dishes = restaurant['Dishes']
    dishes = sorted(dishes, key=lambda k: k['Score'])
    dish_names = [dish['Name'] for dish in dishes]

    return json.dumps(dish_names)