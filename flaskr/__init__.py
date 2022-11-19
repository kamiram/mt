import os
import json
from uuid import uuid4
from flask import Flask, render_template, g, request, current_app, Response
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

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
            cur.execute(
                'UPDATE email SET read=current_timestamp, readcount=:readcount WHERE uid=:uid', 
                dict(uid=uid, readcount=email['readcount'] + 1)
            )
        cur.close()
        db.get_db().commit()
        return ''

    @app.route('/link', methods=['POST'])
    def link():
        # print(request.get_data())
        data = json.loads(request.get_data())
        data['uid'] = uid = uuid4().hex
        cur = db.get_db().cursor()
        cur.execute(
            'INSERT INTO email (uid, mail_from, mail_to, topic) VALUES (:uid, :mail_from, :mail_to, :topic)', 
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

    return app
