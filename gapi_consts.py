from os import environ
from json import dump, load, loads

# App Constants
#   Each constant below is defined as a function return value so that it
# remains constant.

# GAJ = Google API JSON
# GAJEV = GAJ environment variable


# Retrieve GAJ environment variable name.
def gajEVName():
    return 'GAJEV'


# Retrieve GAJ file name, a name with an air of mystery.
def gajFileName():
    return 'gaj.dat'


if environ.get(gajEVName()) is None:
    try:
        with open(gajFileName(), 'r') as inFile:
            GAJdict = load(inFile)
    except FileNotFoundError:
        print("\nException: \n" +
              "There was no environment variable \"{}\"".format(gajEVName()) +
              " and the file \"{}\" was not found.\n".format(gajFileName()))
        raise SystemExit
else:
    # Convert environment variable holding GAJ into a Python dictionary.
    #   os.environ.get loads GAJEV as a string. json.loads converts a JSON
    #   string into a Python dictionary.
    GAJdict = loads(environ.get(gajEVName()))

    # Write dictionary holding JSON to ".json" file since
    # google_auth_oauthlib.flow.Flow requires that such a ".json" file exists.
    with open(gajFileName(), 'w') as outfile:
        dump(GAJdict, outfile)


# Retrieve GAJ as a Python dictionary.
def gaj():
    return GAJdict


# Google API user permission scopes for Google authentication and Oauth2 API.
def gapiScopes():
    return ['openid',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email']


# Google Oauth2 API specs
def gapiOauth():
    return {'name': 'oauth2', 'version': 'v2'}
