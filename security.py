from models.user import UserModel

def authenticate(username, password):
    """This function authenticates a user.
        Given a user name and a password,
        this fn will select the correct username from our list.
    """
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload): # payload is the contents of the JWT token
    user_id = payload['identity'] # extract userid from the payload
    return UserModel.find_by_id(user_id)
