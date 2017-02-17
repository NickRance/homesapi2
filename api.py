#Address
#Picture Url

from flask import Flask
from flask_restful import Resource, Api, request
import json
import os
import types
import requests
import sys


app = Flask(__name__)
api = Api(app)


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

api.route = types.MethodType(api_route, api)

@api.route('/matches')
class Server(Resource):
    def get(self):
        output_dict = generate_matches()
        #number = request.args.get('number')
        return output_dict
        #print(data,file=sys.stderr)

#api.route('/homes')
class homes(Resource):
    def get(self):
        iter =0
        count = 0
        number = request.args.get('number')
        zipCode = request.args.get('zipcode')
        #print(zipCode)
        #print(number)
        output_dict = {}
        with open('bigdump2.json') as data_file:
            data = json.load(data_file)
        while count <= int(number):
            #print("Iter: "+str(iter))
            #print(data[iter][0]["address"]["postal_code"]["value"])
            if data[iter][0]["address"]["postal_code"]["value"] == zipCode:
                output_dict[count] = data[iter][0]
                count+=1
                output_dict[count]["food_score"] = getYelpRestaurants(data[iter][0]["address"]["postal_code"]["value"])
            iter+=1

        return output_dict
                #print(data,file=sys.stderr)
api.add_resource(homes, '/homes')

def generate_matches():
    output_dict = {}
    with open('bigdump2.json') as data_file:
        data = json.load(data_file)
    # for iter in range(0,int(number)):
   # print(data[0])
    for iter in range(0, 5):
        output_dict[iter] = getMatchFields(data[iter][0])
    return output_dict

def getMatchFields(listing):
    """
    :param listing: Accepts the a listing and returns a list with only the fields needed to display a match
    :return:
    """
    #print(listing)
    clean_record = {}
    clean_record["street_address"] = listing["address"]["street_address"]["label"]
    clean_record["postal_code"] = listing["address"]["postal_code"]["value"]
    clean_record["city"] = listing["address"]["locality"]["label"]
    clean_record["state"] = listing["address"]["region"]["label"]
    clean_record["main_uri"] = "http://homes.com" + listing["main_uri"]
    clean_record["price"] = listing["price"]["value"]
    clean_record["primary_image "] = listing["primary_image"]["src"]
    clean_record["crime_url"] = getCrimeUrl(listing["address"]["postal_code"]["value"])
    clean_record["food_score"] = getYelpRestaurants(listing["address"]["postal_code"]["value"])
    clean_record["restaurant_search_url"] = "https://www.yelp.com/search?find_desc=Restaurants&find_loc="+listing["address"]["postal_code"]["value"]
    return clean_record
#api.add_resource(Server, '/')
def getCrimeUrl(zipcode):
    return ("http://www.mylocalcrime.com/#"+zipcode)

def getYelpRestaurants(zipcode):
    url = "https://api.yelp.com/v3/businesses/search"

    querystring = {"term": "restaurants", "location": zipcode, "sort_by": "rating"}

    headers = {
        'authorization': "Bearer kqvOVDOQeslDhIResy4ITpm1koTAGKnzQTOgQE80hYk-cIxKc9_g4sZSAY4e5VhUnVZlg9UZU8p7nTw3fKNpsW49cucrvvki-M8VEg1Uz_J-Fjg-bda49n8HOKumWHYx",
        'cache-control': "no-cache",
        'postman-token': "08286f44-b75a-b265-e966-40e016de51bd"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    #print(response)
    sum=0
    for business in response["businesses"]:
        sum += business['rating']
    return (sum/len(response["businesses"]))

if __name__ == '__main__':
    app.run(debug=True, host = os.getenv("IP","0.0.0.0"),port = int (os.getenv('PORT', 33507)))
    #app.run()