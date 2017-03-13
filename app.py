import json
from flask import Flask, request, redirect, render_template, url_for
from pathlib import Path
from oauth_client import OAuthClient

app = Flask(__name__)
oauth = OAuthClient()


@app.route("/")
def index():
    # Rendering if site is installed.
    if Path("photolog.cfg").is_file():
        content = oauth.request()
        j = json.loads(content)

        return render_template('index.html', photo=j['photos']['photo'])
    else:
        # Redirect to getting access token page.
        return redirect(url_for('install'))


@app.route("/install")
def install():
    return render_template('install.html')


@app.route("/oauth/access", methods=['POST'])
def oauth_access():
    oauth.init_consumer(key=request.form.get('key'), secret=request.form.get('secret'))
    oauth.callback_url = request.form.get('callback_url')

    token = oauth.request_token()
    authorize_url = oauth.get_authorize_url(token)
    return redirect(authorize_url)


@app.route("/oauth/callback")
def oauth_callback():
    access_token = oauth.callback(oauth_token=request.args['oauth_token'], verifier=request.args['oauth_verifier'])
    return str(access_token)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
