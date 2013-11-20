import random
import requests
from flask import request as req, redirect, session, url_for
from flask_oauth import OAuth
from settings import *


oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_API_SECRET,
    request_token_params=PERMISSIONS
)


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')


def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)


################# Old module interface  #########################
"""
Notes.
Since 2011 Facebook drops oAuth 1.0 support in exchange
for oAuth2.0.
Following to oAuth 2.0 protocol RFC:

1) @gen_token function become redundant;
2) oauth tokens becomes "short-lived" (storing tokens somewhere
    can be skipped);

Module interface has been retained for functional sepparation, but not
gurantee compatibility (means same function behaviour) with LinkedIn o
auth module.
"""

def create_oauth_consumer():
    return oauth._consumer


def login():
    return facebook.authorize(callback=url_for('handle_callback',
        next=req.args.get('next'), _external=True))


@facebook.authorized_handler
def handle_callback(resp):
    next_url = req.args.get('next') or url_for('home')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')
    return redirect(next_url)


## no longer actual
def gen_token():
    raise


def get_base_url():
    return  url_for('home')


def scrape_and_process_profile(app, closure):
    result = requests.get( GET_FRIENDS_URL %
                            session['facebook_token'][0])

    friends_resp = result.json()
    try:
        data = friends_resp['data']
        if not data:
            return closure(non_found=True)
        friend = random.choice(data)
    except LookupError as e:  # (KeyError, IndexError)
        app.logger.warning('Something wrong with api response %r'
                           % friends_resp)
        return closure(bad_token=True)

    uid = friend['id']
    api_url  = GET_FRIEND_INFO % (uid, session['facebook_token'][0],)

    result = requests.get(api_url)
    return closure(person=result.json(),
                   look_up_names = look_up_names)
