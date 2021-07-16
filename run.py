import os
import json
from flask import Flask, jsonify, abort, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from flask_cors import CORS

# --- INFO: APP CONFIGURATION ---

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] =  os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- INFO: DATABASE MODEL ---

class Colors(db.Model):
    color_code = Column(Integer, primary_key=True)
    color_name = Column(String(100), nullable=False)

class Countries(db.Model):
    country_code = Column(Integer, primary_key=True)
    country_name = Column(String(100), nullable=False)

class Regions(db.Model):
    region_code = Column(Integer, primary_key=True)
    region_name = Column(String(100), nullable=False)

class Varieties(db.Model):
    variety_code = Column(Integer, primary_key=True)
    variety_name = Column(String(100), nullable=False)

class Vineyards(db.Model):
    vineyard_code = Column(Integer, primary_key=True)
    vineyard_name = Column(String(100), nullable=False)

class Villages(db.Model):
    village_code = Column(Integer, primary_key=True)
    village_name = Column(String(100), nullable=False)

class Years(db.Model):
    year_number = Column(Integer, primary_key=True)

class Wines(db.Model):
    wine_id = Column(Integer, primary_key=True)
    wine_name = Column(String(40), nullable=True)
    wine_description = Column(String(100), nullable=True)
    origin = Column(String(100), nullable=True)
    price = Column(Float, nullable=True)
    color_code = Column(Integer, ForeignKey(Colors.color_code), nullable=False)
    country_code = Column(Integer, ForeignKey(Countries.country_code), nullable=False)
    region_code = Column(Integer, ForeignKey(Regions.region_code), nullable=False)
    variety_code = Column(Integer, ForeignKey(Varieties.variety_code), nullable=False)
    vineyard_code = Column(Integer, ForeignKey(Vineyards.vineyard_code), nullable=False)
    village_code = Column(Integer, ForeignKey(Villages.village_code), nullable=False)
    year_number = Column(Integer, ForeignKey(Years.year_number), nullable=False)

class Image(db.Model):
    image_id = Column(Integer, primary_key=True)
    wine_id = Column(Integer, ForeignKey(Wines.wine_id), nullable=False)
    url = Column(String(200), nullable=False)

   

# --- INFO: FUNCTIONS ---

# --- INFO: ROUTES ---

@app.route('/')
def home():
    return render_template('documentation.html', title='Documentation')

if __name__ == '__main__':
    app.run(debug=True)