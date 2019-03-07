# App Constants
#   Each is defined as a function return value so that it remains constant.


# Google API project data file name
def gpdFileName():
    return 'gapiProject.dat'


# Google API user permission scopes for Google Sign-In
def gapiGSIscopes():
    return ['https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email', 'openid']


# Main subject of notes
#   Return the subject of the notes as a string. This string is not defined in
#   the database, until a feature is added to enable an admin to specify it.
def subject():
    return "Deep Learning"
