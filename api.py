#Address
#Picture Url

from flask import Flask
from flask_restful import Resource, Api, request
import json
import os
import types
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

def generate_matches():
    output_dict = {}
    with open('bigdump2.json') as data_file:
        data = json.load(data_file)
    # for iter in range(0,int(number)):
   # print(data[0])
    for iter in range(0, 10):
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
    clean_record["state"] = listing["address"]["region"]["label"]
    clean_record["main_uri"] = listing["main_uri"]
    clean_record["price"] = listing["price"]["value"]
    clean_record["primary_image "] = listing["primary_image"]["src"]
    return clean_record
#api.add_resource(Server, '/')

if __name__ == '__main__':
    app.run(debug=True, host = os.getenv("IP","0.0.0.0"),port = int (os.getenv('PORT', 33507)))
    #app.run()