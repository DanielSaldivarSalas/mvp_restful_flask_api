from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "Nicholas",
        "age": 42,
        "occupation": "Network Engineer"
    },
    {
        "name": "Elvin",
        "age": 32,
        "occupation": "Doctor"
    },
    {
        "name": "Jass",
        "age": 22,
        "occupation": "Web Developer"
    }
]


class User(Resource):

    def get(self, name):

        for user in users:
            if(name == user["name"]):
                return user, 200
        
        #if name does not exist, return 404 error not found
        return "User does not exist".format(name), 404
    
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()
        
        #user already exists?
        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }

        users.append(user)
        return user, 201

    def put(self, name):
        '''
        put updates user
        if user does not exist, create it
        '''
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        #update if user exists
        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200

        #if user does not exist, create it
        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }

        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name ]

        return "{} is deleted".format(name), 200

api.add_resource(User, "/user/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)