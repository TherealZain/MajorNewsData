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
techcrunch_articles = webScraper.fetchTechCrunchSections("https://techcrunch.com/category/artificial-intelligence/")
investopedia_articles = webScraper.fetchInvestopedia( "https://www.investopedia.com/", "finance")
yahooFinance_articles = webScraper.fetchYahooFinance(
    "https://finance.yahoo.com/", "finance")


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


@app.route('/get_articles_cnn', methods=['GET'])
def api_fetch_cnn_articles():
    source = request.args.get('source', 'all')

    if source in all_articles:
        response = jsonify(all_articles[source])
    elif source == 'all':
        response = jsonify(all_articles)
    else:
        response = jsonify({"error": "Invalid source"}), 400

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
    

@app.route('/get_articles_techcrunch', methods=['GET'])
def api_fetch_techcrunch_articles():
    return jsonify(techcrunch_articles)


# Define a route to fetch Investopedia articles
@app.route('/get_articles_investopedia', methods=['GET'])
def api_fetch_investopedia_articles():
    return jsonify(investopedia_articles)


# Define a route to fetch Yahoo Finance articles
@app.route('/get_articles_yahoofinance', methods=['GET'])
def api_fetch_yahoofinance_articles():
    return jsonify(yahooFinance_articles)


if __name__ == '__main__':
    with app.app_context():
        print("Executing code inside the app context...")
        print("Current app instance: ", flask.current_app)
    app.run()
