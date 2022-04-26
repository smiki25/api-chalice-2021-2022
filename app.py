"""
program
"""
import uuid
import json
import boto3


from chalice import UnauthorizedError, Chalice
from chalicelib import users, authorizer, places
from boto3.dynamodb.conditions import Key
from chalicelib.secrets_manager import get_secret


app = Chalice(app_name='Explore')
app.debug = True
dynamodb = boto3.resource("dynamodb")
secret = get_secret()


def get_app_db(name_table):
    """
    :param name_table:.
    :return:
    """
    return dynamodb.Table(name_table)


def user_exists(email):
    """
    Determines if the email address is already registered
    Function :
        user_exists(email)
    Return :
        JSON/Boolean
    """
    try:
        response = get_app_db('users').query(
            KeyConditionExpression=Key('email').eq(email)
        )
        return response['Items'][0]
    except Exception:
        return False


@app.authorizer()
def jwt_authorizer(auth_request):
    return authorizer.authorize_request(auth_request)


@app.route('/me',
           methods=['PUT'],
           authorizer=jwt_authorizer)
def update_user():
    data = app.current_request.json_body
    email_jwt = app.current_request.context['authorizer']['principalId']
    response = user_exists(email_jwt)
    if response:
        return users.update_user(email_jwt, data, response)


@app.route('/me',
           methods=['GET'],
           authorizer=jwt_authorizer)
def user_details():
    email_jwt = app.current_request.context['authorizer']['principalId']
    response = user_exists(email_jwt)
    if response:
        return safe_serialize(response)
    raise UnauthorizedError('no_such_user')


@app.route('/example', #'/example' is our entry point
           methods=['PUT']) #methods PUT is the request we are sending
def example_endpoint():
    try:
        request = app.current_request
        data = request.json_body
        get_app_db('users').update_item(
            Key={'email': data['email']},
            UpdateExpression="set fullname = :fn",
            ExpressionAttributeValues={
                ':fn': data['fullname']
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        return {'Message': str(e)}

@app.route('/register',
           methods=['POST'])
def register():
    """
    Registration of users into DynamoDB while validating Email Addresses and Encrypting Passwords using Bcrypt
    Resource :
         /register

     Function :
         register()

     Return :
         JSON
    """
    request = app.current_request
    data = request.json_body
    return users.register(data)


@app.route('/login',
           methods=['POST'])
def login():
    """
     Login authentication of registered users and the provision of a JWT token with a basic payload
     Function :
         login()

     Return :
         JWT
     """
    request = app.current_request
    data = request.json_body
    return users.login(data)


def safe_serialize(obj):
    """
    serializes un-serializable data
    Function :
        safe_serialize(obj)

    Return :
        JSON
    """
    default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"
    return json.dumps(obj, default=default)


@app.route('/place', methods=['POST'], authorizer=jwt_authorizer)
def add_place():
    """
    Resource: /place

    Function : add_place()

    Description : Creates new object into places table

    Return : Dict
    """
    data = app.current_request.json_body
    coordinates = data.get('coordinates')
    return places.add_place(data, coordinates)


@app.route('/places/{placeID}', methods=['GET'])
def place_details(placeID):
    """
    Resource: /places/{placeID}

    Function : place_details(placeID)

    Description : Gets all information for object based on the place id taken from the URL

    Return :
    """
    return places.place_details(placeID)


@app.route('/places/{placeID}', methods=['PUT'], authorizer=jwt_authorizer)
def place_details_update(placeID):
    data = app.current_request.json_body
    places.place_details_update(placeID, data)


@app.route('/me/wishlist', methods=['POST'], authorizer=jwt_authorizer)
def add_wishList():
    """
    Resource: /me/wishlist

    Function : add_wishList()

    Description : Adds object to wishList table.

    Return : Dict
    """
    data = app.current_request.json_body
    return places.add_wishList(data)


@app.route('/me/wishlist', methods=['GET'])
def get_wishList():
    """
    Resource: /me/wishlist

    Function : get_wishList()

    Description : Gets all objects and their information from wishList table

    Return : Dict
    """
    data = app.current_request.json_body
    return places.get_wishList(data)


@app.route('/me/like', methods=['POST'], authorizer=jwt_authorizer)
def add_likedPlace():
    """
    Resource: /me/like

    Function : add_likedPlace()

    Description : Adds object to the likedPlaces table.

    Return : Dict
    """
    data = app.current_request.json_body
    return places.add_likedPlace(data)


@app.route('/me/like', methods=['GET'])
def get_list_likedPlace():
    """
    Resource: /me/like

    Function : get_list_likedPlace()

    Description : Gets all objects from likedPlaces table.

    Return :
    """
    data = app.current_request.json_body
    return places.get_list_likedPlaces(data)


@app.route('/me/places_added', methods=['POST'], authorizer=jwt_authorizer)
def me_placesAdded():
    """
    Resource: /me/places_added

    Function : me_placesAdded()

    Description : Adds object to placesAdded table.

    Return : Dict
    """
    data = app.current_request.json_body
    return places.me_placesAdded(data)


@app.route('/me/places_added', methods=['GET'])
def get_me_placeAdded():
    """
    Resource: /me/places_added

    Function : get_me_placeAdded()

    Description : Gets all objects and their information from placesAdded table.

    Return :
    """
    data = app.current_request.json_body
    return places.get_me_placesAdded(data)


@app.route('/me/visit', methods=['POST'], authorizer=jwt_authorizer)
def add_placesVisited():
    """
    Resource: /me/visit

    Function : add_placesVisited()

    Description : Adds object to placesVisited table.

    Return : Dict
    """
    data = app.current_request.json_body
    return places.add_placesVisited(data)


@app.route('/me/visited', methods=['GET'])
def get_list_placeVisited():
    """
    Resource: /me/visited

    Function : list_placeVisited()

    Description : Gets all objects and their information from visitedPlaces table.

    Return :
    """
    data = app.current_request.json_body
    return places.get_list_placesVisited(data)


@app.route('/place',
           methods=['GET'])
def list_place():
    """
    def
    :return:
    """
    try:
        return get_app_db('Places').scan().get('Items')
    except Exception as e:
        return {'Message': str(e)}
