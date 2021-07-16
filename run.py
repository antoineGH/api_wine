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

    def __repr__(self):
            return "color_code: {}, color_name: {}".format(self.color_code, self.color_name)

class Countries(db.Model):
    country_code = Column(Integer, primary_key=True)
    country_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "country_code: {}, country_name: {}".format(self.country_code, self.country_name)

class Regions(db.Model):
    region_code = Column(Integer, primary_key=True)
    region_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "region_code: {}, region_name: {}".format(self.region_code, self.region_name)

class Varieties(db.Model):
    variety_code = Column(Integer, primary_key=True)
    variety_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "variety_code: {}, variety_name: {}".format(self.variety_code, self.variety_name)

class Vineyards(db.Model):
    vineyard_code = Column(Integer, primary_key=True)
    vineyard_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "vineyard_code: {}, vineyard_name: {}".format(self.vineyard_code, self.vineyard_name)

class Villages(db.Model):
    village_code = Column(Integer, primary_key=True)
    village_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "village_code: {}, village_name: {}".format(self.village_code, self.village_name)

class Years(db.Model):
    year_number = Column(Integer, primary_key=True)

    def __repr__(self):
        return "year_number: {}".format(self.year_number)

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
    image = db.relationship('Image', backref='image', lazy=True)

    def __repr__(self):
        return "wine_id: {}, wine_name: {}, wine_description: {}, origin: {}, price: {}, color_code: {}, country_code: {}, region_code: {}, variety_code: {}, vineyard_code: {}, village_code: {}, year_number: {}, image: {}".format(self.wine_id, self.wine_name, self.wine_description, self.origin, self.price, self.color_code, self.country_code, self.region_code, self.variety_code, self.vineyard_code, self.village_code, self.year_number, self.image)

    @property
    def serialize(self):
        color_code = Colors.query.get(self.color_code).color_name
        country_code = Countries.query.get(self.country_code).country_name
        region_code = Regions.query.get(self.region_code).region_name
        variety_code = Varieties.query.get(self.variety_code).variety_name
        vineyard_code = Vineyards.query.get(self.vineyard_code).vineyard_name
        village_code = Villages.query.get(self.village_code).village_name
        year_number = Years.query.get(self.year_number).year_number
        # image = Image.query.get(self.wine_id).url
        images = Image.query.filter_by(wine_id=self.wine_id).all()
        print(images)

        
        return {
            'wine_id': self.wine_id,
            'wine_name': self.wine_name,
            'wine_description': self.wine_description,
            'origin': self.origin,
            'price': self.price,
            'color_name': color_code,
            'country_name': country_code,
            'region_name': region_code,
            'variety_name': variety_code,
            'vineyard_name': vineyard_code,
            'village_name': village_code,
            'year_number': year_number,
            'images': [image.url for image in images],
        }

class Image(db.Model):
    image_id = Column(Integer, primary_key=True)
    wine_id = Column(Integer, ForeignKey(Wines.wine_id), nullable=False)
    url = Column(String(200), nullable=False)

    def __repr__(self):
        return "image_id: {}, wine_id: {}, url: {}".format(self.image_id, self.wine_id, self.url)

# --- INFO: FUNCTIONS ---

# --- INFO: ROUTES ---

@app.route('/')
def home():
    return render_template('documentation.html', title='Documentation')

@app.route('/api/wines', methods=['GET'])
def get_products():
    wines = Wines.query.all()
    return jsonify([wine.serialize for wine in wines])


if __name__ == '__main__':
    app.run(debug=True)