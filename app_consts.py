import json

# App Constants
#   Each is defined as a function return value so that it remains constant.

# Extract Google API project data (GPD) from file and store in dict.
with open('gapiProject.dat', 'r') as gpdFile:
    GPD = json.load(gpdFile)


# gpd
#  Returns the project's associated Google API data in a dict.
def gpd():
    return GPD


# subject
#   Returns the subject of the notes as a string. This string is not defined in
#   database, until a feature is added to enable user to specify it.
def subject():
    return "Deep Learning"
