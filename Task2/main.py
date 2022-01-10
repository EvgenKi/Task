from flask import Flask, render_template, request, redirect, session, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'ab8864324cdd19735e0740ea255025db983a2315'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def create_request():
    if request.method == "POST":
        clear_session()
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user = User.query.filter_by(first_name=first_name, last_name=last_name).first()
        session['is_user_create'] = False
        if not user:
            user = User(first_name=first_name, last_name=last_name)
            db.session.add(user)
            db.session.commit()
            session['is_user_create'] = True

        session['id'] = user.id
        return redirect('/greetings')

    return render_template("home.html")


@app.route('/list')
def welcome_list():
    page = request.args.get('page')
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1

    users = User.query.order_by(User.first_name)
    pages = users.paginate(page=page, per_page=6)
    return render_template("list.html", pages=pages)


@app.route('/greetings')
def greetings():
    user_id = session.get('id')
    if user_id is None:
        abort(403)
    user = User.query.get(user_id)
    greeting = (
        f'Nice to meet you,{user.first_name} {user.last_name}'
        if session.get('is_user_create')
        else f'Hi again,{user.first_name} {user.last_name}'
    )
    clear_session()
    return render_template("gre.html", greeting=greeting)


def clear_session():
    session.pop('id', None)
    session.pop('is_user_create', None)


if __name__ == "__main__":
    app.run(debug=True)
