from flask import Flask, request, jsonify
from pymongo import MongoClient 
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# MY_ENV_VAR = os.getenv('MY_ENV_VAR')


MONGO_URI = os.environ.get('MONGO_URI')

cluster = MongoClient(MONGO_URI)
db = cluster['chidam_city_db']
col = db['city_collection']

def get_city_data():
    # last_movie_id = col.find().sort([('movie_id', -1)]).limit(1)
    city_id  = col.find().sort([('city_id', -1)]).limit(1)
    print(city_id)
    try:
        city_id = city_id[0]['city_id']
    except:
        city_id = 0

    return city_id


@app.route("/", methods=['POST'])
def startpy():

    city = request.json['city']
    province = request.json['province']    
    country = request.json['country']
    
    last_city_id = get_city_data()
    print(last_city_id)
    current_city_id = int(last_city_id) + 1

    city_dict = {

        "city_id": current_city_id,
        "city_name": city,
        "city_province": province,
        "city_country": country

    }
    col.insert_one(city_dict)
    return "success"

   
@app.route("/get", methods=['GET'])
def get_all_city():
    city_dict = []
    city = col.find()
    print(city)

    city_list = []

    for item in city:

        city_dict = {
            "city_id": item['city_id'],
            "city_name": item['city_name'],
            "city_province": item['city_province'],
            "city_country": item['city_country']

        }

        city_list.append(city_dict)
        print(item)    
    return jsonify(city_list)


@app.route("/get/<city_id>", methods=['GET'])
def get_one_city(city_id):

    city = col.find_one({'city_id': int(city_id)})
    print(city)

   
    city_dict = {
            "city_id": city['city_id'],
            "city_name": city['city_name'],
            "city_province": city['city_province'],
            "city_country": city['city_country']

    }
    return city_dict


@app.route("/edit/<city_id>", methods=['POST'])
def edit_city(city_id):
    # movie = col.find_one({'movie_id': int(movie_id)})

    city = province = request.json['city']  
    province = request.json['province']    
    country = request.json['country']
    

    city_dict = {

        "city_id": int(city_id),
        "city_name": city,
        "city_province": province,
        "city_country": country

    }

    col.update_many({'city_id': int(city_id)}, {'$set': city_dict})
    
    return 'success'
    
@app.route("/delete/<city_id>", methods=['DELETE'])
def delete_one_city(city_id):
    print(city_id)
    col.delete_many({'city_id': int(city_id)})

    return 'fail'

if __name__ == "__main__":
    app.run(debug=True)