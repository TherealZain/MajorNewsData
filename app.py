import flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import webScraper
from flask import request, jsonify
import os



app = flask.Flask(__name__)
app.secret_key = 'cloud9typebeat'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db= SQLAlchemy(app)

cnn_articles = webScraper.fetchCNN("https://www.cnn.com/business/tech", "tech")

all_articles = {
    "cnn": cnn_articles
}

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    major = db.Column(db.String(120), nullable = False)
    email = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Name %r>' % self.name


with app.app_context():
    print("Executing code inside the app context...")
    print("Current app instance: ", flask.current_app)
    db.create_all()


@app.route('/')
def helloWorld():
    return 'Hello World'


@app.route('/get_articles', methods=['GET'])
def api_fetch_all_articles():
    source = request.args.get('source', 'all')

    if source in all_articles:
        return jsonify(all_articles[source])
    elif source == 'all':
        return jsonify(all_articles)
    else:
        return jsonify({"error": "Invalid source"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
