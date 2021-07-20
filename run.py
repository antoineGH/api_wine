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

    @property
    def serialize(self):
        
        return {
            'color_code': self.color_code,
            'color_name': self.color_name,
        }

class Countries(db.Model):
    country_code = Column(Integer, primary_key=True)
    country_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "country_code: {}, country_name: {}".format(self.country_code, self.country_name)

    @property
    def serialize(self):
        
        return {
            'country_code': self.country_code,
            'country_name': self.country_name,
        }

class Regions(db.Model):
    region_code = Column(Integer, primary_key=True)
    region_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "region_code: {}, region_name: {}".format(self.region_code, self.region_name)

    @property
    def serialize(self):
        
        return {
            'region_code': self.region_code,
            'region_name': self.region_name,
        }

class Varieties(db.Model):
    variety_code = Column(Integer, primary_key=True)
    variety_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "variety_code: {}, variety_name: {}".format(self.variety_code, self.variety_name)

    @property
    def serialize(self):
        
        return {
            'variety_code': self.variety_code,
            'variety_name': self.variety_name,
        }

class Vineyards(db.Model):
    vineyard_code = Column(Integer, primary_key=True)
    vineyard_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "vineyard_code: {}, vineyard_name: {}".format(self.vineyard_code, self.vineyard_name)

    @property
    def serialize(self):
        
        return {
            'vineyard_code': self.vineyard_code,
            'vineyard_name': self.vineyard_name,
        }

class Villages(db.Model):
    village_code = Column(Integer, primary_key=True)
    village_name = Column(String(100), nullable=False)

    def __repr__(self):
            return "village_code: {}, village_name: {}".format(self.village_code, self.village_name)

    @property
    def serialize(self):
        
        return {
            'village_code': self.village_code,
            'village_name': self.village_name,
        }

class Years(db.Model):
    year_number = Column(Integer, primary_key=True)

    def __repr__(self):
        return "year_number: {}".format(self.year_number)

    @property
    def serialize(self):
        
        return {
            'year_number': self.year_number,
        }

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
        images = Image.query.filter_by(wine_id=self.wine_id).all()
        
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

# --- INFO: ROUTES ---

@app.route('/')
def home():
    return render_template('documentation.html', title='Documentation')

@app.route('/api/varieties', methods=['GET'])
def get_varieties():
    varieties = Varieties.query.all()
    if not varieties:
        return jsonify({"message": "No variety in database"})
    return jsonify([variety.serialize for variety in varieties])

@app.route('/api/variety/<variety_id>', methods=['GET'])
def get_variety(variety_id):
    if not variety_id:
        return jsonify({"message": "Variety ID missing"}), 404
    variety = Varieties.query.get(variety_id)
    if not variety:
        return jsonify({"message": "Variety doesn\'t exist"}), 404
    return jsonify(variety.serialize)


@app.route('/api/years', methods=['GET'])
def get_years():
    years = Years.query.all()
    if not years:
        return jsonify({"message": "No year in database"}), 404
    return jsonify([year.serialize for year in years])

@app.route('/api/year/<year_number>', methods=['GET'])
def get_year(year_number):
    if not year_number:
        return jsonify({"message": "Year Number missing"}), 404
    year = Years.query.get(year_number)
    if not year:
        return jsonify({"message": "Year doesn\'t exist"}), 404
    return jsonify(year.serialize)

@app.route('/api/villages', methods=['GET'])
def get_villages():
    villages = Villages.query.all()
    if not villages:
        return jsonify({"message": "No village in database"}), 404
    return jsonify([village.serialize for village in villages])

@app.route('/api/village/<village_id>', methods=['GET'])
def get_village(village_id):
    if not village_id:
        return jsonify({"message": "Village ID missing"})
    village = Villages.query.get(village_id)
    if not village:
        return jsonify({"message": "No village in database"})
    return jsonify(village.serialize)

@app.route('/api/regions', methods=['GET'])
def get_regions():
    regions = Regions.query.all()
    if not regions:
        return jsonify({"message": "No region in database"}), 404
    return jsonify([region.serialize for region in regions])

@app.route('/api/region/<region_id>', methods=['GET'])
def get_region(region_id):
    if not region_id:
        return jsonify({"message": "Region ID missing"}), 404
    region = Regions.query.get(region_id)
    if not region:
        return jsonify({"message": "Region doesn\'t exist"}), 404   
    return jsonify(region.serialize)

@app.route('/api/countries', methods=['GET'])
def get_countries():
        countries = Countries.query.all()
        if not countries:
            return jsonify({"message": "No country in database"}), 404
        return jsonify([country.serialize for country in countries])

@app.route('/api/country/<country_id>', methods=['GET'])
def get_country(country_id):
    if not country_id:
         return jsonify({'message': 'Country ID missing'}), 404
    country = Countries.query.get(country_id)
    if not country:
        return jsonify({"message": "Country doesn\'t exist"}), 404
    return jsonify(country.serialize)

@app.route('/api/colors', methods=['GET'])
def get_colors():
    colors = Colors.query.all()
    if not colors:
        return jsonify({"message": 'No color in database'}), 404
    return jsonify([color.serialize for color in colors])

@app.route('/api/color/<color_id>', methods=['GET'])
def get_color(color_id):
    if not color_id:
        return jsonify({'message': 'Color ID missing'}), 404
    color = Colors.query.get(color_id)
    if not color:
        return jsonify({'message': 'Color doesn\'t exist'}), 404
    return jsonify(color.serialize)

@app.route('/api/wines', methods=['GET', 'POST'])
def get_wines():
    if request.method == "GET":
        wines = Wines.query.all()
        if not wines:
            return jsonify({'message': 'No wine in database'}), 404
        return jsonify([wine.serialize for wine in wines])
    
    if request.method == "POST":
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400

        content = request.get_json(force=True)
        wine_name = content.get('wine_name', None)
        wine_description = content.get('wine_description', None)
        origin = content.get('origin', None)
        price = content.get('price', None)
        color_code = content.get('color_code', None)
        country_code = content.get('country_code', None)
        region_code = content.get('region_code', None)
        variety_code = content.get('variety_code', None)
        vineyard_code = content.get('vineyard_code', None)
        village_code = content.get('village_code', None)
        year_number = content.get('year_number', None)

        if not wine_name:
            return jsonify({"message": "Missing wine_name"}), 400

        if not wine_description:
            return jsonify({"message": "Missing wine_description"}), 400

        if not origin:
            return jsonify({"message": "Missing origin"}), 400

        if not price:
            return jsonify({"message": "Missing price"}), 400

        if not color_code:
            return jsonify({"message", "Missing color_code"}), 400

        if not country_code:
            return jsonify({"message": "Missing country_code"}), 400
        
        if not region_code:
            return jsonify({"message": "Missing region_code"}), 400

        if not variety_code:
            return jsonify({"message": "Missing variety_code"}), 400

        if not vineyard_code:
            return jsonify({"message": "Missing vineyard_code"}), 400

        if not village_code:
            return jsonify({"message": "Missing village_code"}), 400

        if not year_number:
            return jsonify({"message": "Missing year_number"}), 400

        wine = Wines(wine_name=wine_name, wine_description=wine_description, origin=origin, price=price, color_code=color_code, country_code=country_code, region_code=region_code, variety_code=variety_code, vineyard_code=vineyard_code, village_code=village_code, year_number=year_number)
        db.session.add(wine)
        db.session.commit()
        return jsonify(wine.serialize)

@app.route('/api/wine/<wine_id>', methods=['GET'])
def get_wine(wine_id):
    if not wine_id:
        return jsonify({'message': 'Wine ID missing'}), 404
    wine = Wines.query.get(wine_id)
    if not wine:
        return jsonify({'message': 'Wine doesn\'t exist'}), 404
    return jsonify(wine.serialize)



if __name__ == '__main__':
    app.run(debug=True)