import json

# App Constants
#   Each constant below is defined as a function return value so that it
# remains constant.


# Google API project data file name
def gpdFileName():
    return 'gapiProject.dat'


# Extract Google API project data (GPD) from file and store it in a dictionary.
with open(gpdFileName(), 'r') as gpdFile:
    GPD = json.load(gpdFile)


# gpd
#  Returns the project's associated Google API data in a dictionary.
def gpd():
    return GPD


# Google API user permission scopes for Google authentication and Oauth2 API.
def gapiScopes():
    return ['openid',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email']


# Google Oauth2 API specs
def gapiOauth():
    return {'name': 'oauth2', 'version': 'v2'}


# Main subject of notes
#   Return the subject of the notes as a string. This string is not defined in
#   the database, until a feature is added to enable an admin to specify it.
def subject():
    return "Deep Learning"
