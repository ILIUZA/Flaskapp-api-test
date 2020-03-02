from werkzeug.security import safe_str_cmp
from models.user import UserModel

'''
When an user calls the /auth endpoint with username and password
: return -- a UserModel object in a successful case 
'''
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

'''
When an user has already authenticated and header is correct
:payload -- a dictionary with  identity-key (id user)
:return -- a UserModel object
'''
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)