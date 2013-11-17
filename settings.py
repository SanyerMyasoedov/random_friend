from utils import make_api_getter, make_permission
import os

## (attribute name, permission name or None)

lookup_fields = [
    ('picture.width(300)', None),
    ('name', 'email'),
    ('gender', None),
    ('education', None),
    ('hometown', 'friends_hometown'),
    ('link',  None),
    ('relationship_status', 'friends_relationships'),
    ('work', 'friends_work_history'),
    ('username', None),
    ('location', 'friends_location'),
    ('music', None),
]

look_up_names  = [p[0] for p in lookup_fields]

GET_FRIEND_INFO = make_api_getter(lookup_fields)
PERMISSIONS = make_permission(lookup_fields)

DEBUG = False


FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']
FACEBOOK_API_SECRET = os.environ['FACEBOOK_API_SECRET']

GET_FRIENDS_URL = 'https://graph.facebook.com/me/friends?access_token=%s'

SECRET_KEY = os.environ['SECRET_KEY']