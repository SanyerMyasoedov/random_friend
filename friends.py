import requests
import random
from flask import Flask, url_for
from flask_oauth import OAuth
from flask import request, session, redirect, render_template
from settings import *



app = Flask(__name__)

app.secret_key = SECRET_KEY
app.debug = DEBUG

oauth = OAuth()



facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_API_SECRET,
    request_token_params={'scope': 'email'}
)


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('home')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')
    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('home'))


@app.route("/")
def home():
    auth = session.get('logged_in', False)

    if not auth:
       return render_template('blueprint.html', login_require=True)

    result = requests.get( GET_FRIENDS_URL %
                            session['facebook_token'][0])

    friends_resp = result.json()
    try:
        data = friends_resp['data']
        if not data:
            return render_template('blueprint.html', non_found=True)
        friend = random.choice(data)
    except LookupError as e:  # (KeyError, IndexError)
        app.logger.warning('Something wrong with returned structure %r'
                           % friends_resp)
        return render_template('blueprint.html', bad_token=True)

    uid = friend['id']
    api_url  = GET_FRIEND_INFO % (uid, session['facebook_token'][0],)

    result = requests.get(api_url)
    return render_template('blueprint.html', person=result.json())


if __name__ == '__main__':
    app.run()
