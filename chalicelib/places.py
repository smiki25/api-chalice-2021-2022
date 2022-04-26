import uuid
from boto3.dynamodb.conditions import Key
import app
from chalicelib.secrets_manager import get_secret


secret = get_secret()


def add_place(data, coordinates):
    try:
        app.get_app_db('places').put_item(Item={
            'Place id ': str(uuid.uuid4()),
            "Image": data['image'],
            "description": data['description'],
            "name": data['name'],
            "latitude": str(coordinates['latitude']),
            "longitude": str(coordinates['longitude'])
        })
    except Exception as e:
        return {'message': str(e)}


def place_details(placeID):
    response = app.get_app_db('places').query(
        KeyConditionExpression=Key('Place id ').eq(placeID)
    )
    items = response.get('Items')[0]
    try:
        return items
    except Exception as e:
        return {'message': str(e)}


def place_details_update(data):
    try:
        app.get_app_db('places').update_item(
            Key={'Place id ': placeID},
            UpdateExpression="set description = :d, longitude = :l, latitude = :a, Image = :i",
            ExpressionAttributeValues={
                ':d': data['description'],
                ':l': data['longitude'],
                ':a': data['latitude'],
                ':i': data['Image']
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        return {'message': str(e)}


def add_wishList(data):
    place = data["place_id"]
    email = data["email"]
    response = app.get_app_db('users').query(
        KeyConditionExpression=Key('email').eq(data["email"])
    )
    wishList = response.get('Items')[0]["wishList"] or set()
    wishList.add(place)
    response = app.get_app_db('users').update_item(
        Key={
            'email': email,
        },
        UpdateExpression="set wishList=:w",
        ExpressionAttributeValues={
            ':w': wishList
        },
        ReturnValues="UPDATED_NEW"
    )
    return list(response["Attributes"]["wishList"])


def get_wishList(data):
    response = app.get_app_db('users').query(
        KeyConditionExpression=Key('email').eq(data["email"])
    )
    items = response.get('Items')[0]["wishList"]
    RequestItems = {
        "places": {
            "Keys": [{"Place id ": place_id} for place_id in items]
        }
    }
    try:
        return dynamodb.batch_get_item(RequestItems=RequestItems)["Responses"]["places"]
    except Exception as e:
        return {'message': str(e)}


def add_likedPlace(data):
    place = data["place_id"]
    email = data["email"]
    response = app.get_app_db('users').query(
        KeyConditionExpression=Key('email').eq(data["email"])
    )
    likedPlaces = response.get('Items')[0]["likedPlaces"]
    likedPlaces.append(place)
    response = app.get_app_db('users').update_item(
        Key={
            'email': email,
        },
        UpdateExpression="set likedPlaces=:l",
        ExpressionAttributeValues={
            ':l': likedPlaces
        },
        ReturnValues="UPDATED_NEW"
    )
    return response["Attributes"]["likedPlaces"]


def get_list_likedPlaces(data):
    response = app.get_app_db('users').query(
        KeyConditionExpression=Key('email').eq(data["email"])
    )
    items = response.get('Items')[0]["likedPlaces"]
    RequestItems = {
        "places": {
            "Keys": [{"Place id ": place_id} for place_id in items]
        }
    }
    try:
        return dynamodb.batch_get_item(RequestItems=RequestItems)["Responses"]["places"]
    except Exception as e:
        return {'message': str(e)}


def me_placesAdded(data):
    place = data["place_id"]
    email = data["email"]
    response = app.get_app_db('users').query(
        KeyConditionExpression=Key('email').eq(data["email"])
    )
    placesAdded = response.get('Items')[0]["placesAdded"]
    placesAdded.append(place)
    response = app.get_app_db('users').update_item(
        Key={
            'email': email,
        },
        UpdateExpression="set placesAdded=:l",
        ExpressionAttributeValues={
            ':l': placesAdded
        },
        ReturnValues="UPDATED_NEW"
    )
    return response["Attributes"]["placesAdded"]


def get_me_placesAdded(data):
    response = app.get_app_db('users').query(
        KeyConditionExpression=Key('email').eq(data["email"])
    )
    items = response.get('Items')[0]["placesAdded"]
    RequestItems = {
        "places": {
            "Keys": [{"Place id ": place_id} for place_id in items]
        }
    }
    try:
        return dynamodb.batch_get_item(RequestItems=RequestItems)["Responses"]["places"]
    except Exception as e:
        return {'message': str(e)}


def add_placesVisited(data):
    place = data["place_id"]
    email = data["email"]
    response = app.get_app_db('users').query(
        KeyConditionExpression=Key('email').eq(data["email"])
    )
    visitedPlaces = response.get('Items')[0]["visitedPlaces"]
    visitedPlaces.append(place)
    response = app.get_app_db('users').update_item(
        Key={
            'email': email,
        },
        UpdateExpression="set visitedPlaces=:v",
        ExpressionAttributeValues={
            ':v': visitedPlaces
        },
        ReturnValues="UPDATED_NEW"
    )
    return response["Attributes"]["visitedPlaces"]


def get_list_placesVisited(data):
    response = app.get_app_db('users').query(
        KeyConditionExpression=Key('email').eq(data["email"])
    )
    items = response.get('Items')[0]["visitedPlaces"]
    RequestItems = {
        "places": {
            "Keys": [{"Place id ": place_id} for place_id in items]
        }
    }
    try:
        return dynamodb.batch_get_item(RequestItems=RequestItems)["Responses"]["places"]
    except Exception as e:
        return {'message': str(e)}

