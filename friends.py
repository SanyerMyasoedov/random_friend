from flask import Flask, url_for
from flask import session, redirect, render_template
from settings import *
from fb_oauth import login, handle_callback, pop_login_session, \
    scrape_and_process_profile


app = Flask(__name__)

app.secret_key = SECRET_KEY
app.debug = DEBUG

app.add_url_rule('/facebook_authorized', view_func=handle_callback)


@app.route("/login")
def facebook_login():
    return login()


@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('home'))


@app.route("/")
def home():
    auth = session.get('logged_in', False)

    if not auth:
       return render_template('blueprint.html', login_require=True)

    render_closure = lambda **k: render_template('blueprint.html', **k)
    return scrape_and_process_profile(app, render_closure)


if __name__ == '__main__':
    app.run()
