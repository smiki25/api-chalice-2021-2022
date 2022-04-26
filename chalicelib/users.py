import jwt
import re
import app

from datetime import datetime, timedelta
from chalicelib import validate_email
from chalicelib.secrets_manager import get_secret
from chalice import UnauthorizedError, ChaliceViewError
from bcrypt import hashpw, gensalt, checkpw


secret = get_secret()


def email_validation(email):
    """
    Function :
        email_validation(email)

    Description :
        Verifies the validity of an email address

    Return :
        Boolean
    """
    return re.match(validate_email.VALID_ADDRESS_REGEXP, email) is not None


def hash_password(password):
    """
    Function :
        hash_password(password)

    Description :
        Hashes the password with generated salt

    Return :
        String
    """
    password = password.encode("utf-8")
    return hashpw(password, gensalt())


def login(data):
    email = data['email']
    password = data['password'].encode("utf-8")
    if email_validation(email):
        response = app.user_exists(email)
        if response:
            if checkpw(password, response['password'].value):
                token = jwt.encode({'data': email, 'exp': datetime.utcnow() + timedelta(days=1)}, secret,
                                   algorithm='HS256')
                return {'token': token}
            else:
                raise UnauthorizedError('email or password is invalid')
        else:
            raise UnauthorizedError('email or password is invalid')
    else:
        raise UnauthorizedError('invalid_email')


def register(data):
    email = data['email']

    if len(data['password']) < 8:
        raise UnauthorizedError("Invalid password")

    if email_validation(email):
        try:
            fullname = data['fullname']
            password = hash_password(data['password'])
        except Exception as e:
            raise UnauthorizedError(e)
    else:
        raise UnauthorizedError('invalid_email_address')

    if app.user_exists(email):
        raise UnauthorizedError('email_already_exists')
    try:
        wishList = {}
        likedList = {}
        app.get_app_db('users').put_item(
            Item={
                'email': email,
                'fullname': fullname,
                'password': password,
                'wishList': wishList,
                'likedList': likedList
            }
        )
        token = jwt.encode({'data': email, 'exp': datetime.utcnow() + timedelta(hours=1)}, secret,
                           algorithm='HS256')
        return {'token': token}
    except Exception as e:
        raise ChaliceViewError(e)


def update_user(email, data, response):
    try:
        fullname = data['fullname']
    except KeyError:
        fullname = response['fullname']
    try:
        wish_list = data['wishList']
    except KeyError:
        wish_list = response['wishList']
    try:
        liked_list = data['likedList']
    except KeyError:
        liked_list = response['likedList']
    try:
        app.get_app_db('users').update_item(
            Key={'email': email},
            UpdateExpression="set fullname = :fn, wishList = :wl, likedList = :ll",
            ExpressionAttributeValues={
                ':fn': fullname,
                ':wl': wish_list,
                ':ll': liked_list,
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        return {'message': str(e)}

