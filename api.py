#Address
#Picture Url

from flask import Flask
from flask_restful import Resource, Api, request
import json
import os
import sys


app = Flask(__name__)
api = Api(app)

class Server(Resource):
    def get(self):
        output_dict = {}
        number = request.args.get('number')
        with open('bigdump2.json') as data_file:
            data = json.load(data_file)
        for iter in range(0,int(number)):
            output_dict[iter] = data[iter]
        return output_dict
        #print(data,file=sys.stderr)


api.add_resource(Server, '/')

if __name__ == '__main__':
    app.run(debug=True, host = os.getenv("IP","0.0.0.0"),port = int (os.getenv('PORT', 33507)))
    #app.run()