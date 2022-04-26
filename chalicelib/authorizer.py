import jwt
import chalice
from chalicelib.secrets_manager import get_secret
secret = get_secret()

def authorize_request(auth_request):
    token = auth_request.token
    parts = token.split()
    if len(parts) == 0 or parts[0] != "Bearer":
        return None
    if len(parts) != 2 or parts[1] == "none":
        return None
    try:
        email_jwt = jwt.decode(parts[1], secret, algorithms=['HS256', ])
    except jwt.exceptions.DecodeError:
        return chalice.AuthResponse(routes=[], principal_id=None, context={})
    return chalice.AuthResponse(routes=['*'], principal_id=email_jwt['data'], context={})


