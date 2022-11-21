import os
import json
from uuid import uuid4

import requests
from flask import (
    Flask,
    redirect,
    request,
    url_for,
    Response,
    current_app,
    render_template
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient

from . import db
from .user import User


def create_app(test_config=None):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='e43ceaf8-6902-11ed-9c92-1b639b2a864c-ed8c0d50-6902-11ed-80c3-670e499fc004',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config.from_pyfile('config.py', silent=False)

    login_manager = LoginManager()
    login_manager.init_app(app)

    client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    def get_google_provider_cfg():
        return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()

    @login_manager.unauthorized_handler
    def unauthorized():
        return "You must be logged in to access this content.", 403

    @app.route('/clear')
    def clear():
        cur = db.get_db().cursor()
        cur.execute('DELETE FROM email ')
        cur.close()
        db.get_db().commit()
        return "cleared"

    @app.route('/emaillog')
    def emaillog():
        cur = db.get_db().cursor()
        emails = cur.execute('SELECT * FROM email ORDER BY sent DESC').fetchall()
        cur.close()
        return render_template('emaillog.html', emaillist=emails)

    @app.route('/t/<uid>')
    def touch(uid):
        print(json.dumps(dict(request.headers), indent=4))
        cur = db.get_db().cursor()
        email = cur.execute('SELECT * FROM email WHERE uid=:uid', dict(uid=uid)).fetchone()
        if email:
            if email['readcount'] >= 0:
                cur.execute(
                    'UPDATE email SET read=current_timestamp, readcount=:readcount WHERE uid=:uid',
                    dict(uid=uid, readcount=email['readcount'] + 1)
                )
            else:
                cur.execute(
                    'UPDATE email SET readcount=0 WHERE uid=:uid',
                    dict(uid=uid)
                )
        cur.close()
        db.get_db().commit()
        return ''

    @app.route('/link', methods=['POST'])
    def link():
        data = json.loads(request.get_data())
        data['uid'] = uid = uuid4().hex
        cur = db.get_db().cursor()
        cur.execute(
            'INSERT INTO email (uid, mail_from, mail_to, topic, readcount) VALUES (:uid, :mail_from, :mail_to, :topic, -1)',
            data
        )
        cur.close()
        db.get_db().commit()
        host_url = current_app.config['HOST_URL']
        resp = Response(response=f'{host_url}{uid}', status=200, mimetype='text/plain')
        resp.headers["Content-Type"] = 'text/plain'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Allow-Headers'] = '*'
        return resp

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            cur = db.get_db().cursor()
            emails = cur.execute('SELECT * FROM email WHERE mail_from=:email ORDER BY sent DESC', dict(email=current_user.email)).fetchall()
            cur.close()
            return render_template('emaillog.html', emaillist=emails, username=current_user.name, email=current_user.email)
        else:
            return redirect('/login')

    @app.route("/login")
    def login():
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        print('cakkback ' + app.config['OAUTH_CALLBACK_URL'])
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=app.config['OAUTH_CALLBACK_URL'],
            scope=["openid", "email", "profile"],
        )

        return redirect(request_uri)

    @app.route("/callback")
    def callback():
        code = request.args.get("code")

        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=app.config['OAUTH_CALLBACK_URL'],
            code=code,
        )

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
        )
        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        print(f'userinfo_response.json() {userinfo_response.json()}')
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            users_name = userinfo_response.json()["given_name"]
            access_token = userinfo_response.json().get("access_token", '')
            id_token = userinfo_response.json().get("id_token", '')
        else:
            return "User email not available or not verified by Google.", 400

        user = User(id_=unique_id, name=users_name, email=users_email, access_token=access_token, id_token=id_token)

        if not User.get(unique_id):
            User.create(unique_id, users_name, users_email, access_token, id_token)

        login_user(user)

        return redirect(url_for("index"))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    return app
