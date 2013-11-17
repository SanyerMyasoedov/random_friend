from utils import make_api_getter

lookup_fields = [
    'picture',
    'name',
    'gender',
    'education',
    'hometown',
    'link',
    'political',
    'religion',
    'relationship_status',
    'work',
    'username',
    'interested_in',
    'movies',
    'location',
    'music',
    'movies',
]

GET_FRIEND_INFO = make_api_getter(lookup_fields)

DEBUG = True

FACEBOOK_APP_ID = '499253193515142'
FACEBOOK_API_SECRET = 'fff847f17a8b653598b3574845ed5b1b'

GET_FRIENDS_URL = 'https://graph.facebook.com/me/friends?access_token=%s'

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'