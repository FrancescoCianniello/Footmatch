#Importation of the necessary libraries
from flask import Flask, request, jsonify #Backend
from flask_cors import CORS #Cross-Origin requests as a security measure
from pymongo import MongoClient #Use of the database
import bcrypt #Password hash library
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity #For the use of JWT as an authentication system

#Flask app configuration
app = Flask("Footmatch")
CORS(app) #Enable for all routes

#Definition of the secret for authentication with JWT
app.config['JWT_SECRET_KEY'] = 'secret_key' #Change with an environment variable
jwt = JWTManager(app) #Initialization of JWT

#Class to manage database connection
class DatabaseManager:
    def __init__(self):
        #Connecting to the mongoDB database
        self.client = MongoClient(
            "mongodb+srv://francesco_cianniello:roberta2022@footmatch.aspfg.mongodb.net/Footmatch?retryWrites=true&w=majority"
        )
        self.db = self.client['footmatch']  #Defining the database name
        self.users_collection = self.db['users']  #Collection creation

#User class to represent users
class User:
    def __init__(self, database_manager):
        self.db_manager = database_manager  #Use of database_manager as a new parameter

#Method for registering a new user
    def registration(self, name, surname, fiscal_code, date_of_birth, username, password):
        #Check that username and password are not blank
        if not username or not password:
            return {"error": "Username and password are required"}, 400

#Check if the user already exists in the database
        if self.db_manager.users_collection.find_one({"username": username}):
            return {"error": "The user already exists"}, 400

    #Password hash
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        #Entering the user into the database
        self.db_manager.users_collection.insert_one({
            "name": name,
            "surname": surname,
            "fiscal_code": fiscal_code,
            "date_of_birth": date_of_birth,
            "username": username,
            "password": hashed_password.decode('utf-8') #Saving the password as a string
        })
        return {"message": "Registration completed"}, 201

#Method for logging in
    def login(self, username, password):
        #Check that username and password are not blank
        if not username or not password:
            return {"error": "Username and password are required"}, 400
#Searching the user in the database
        user = self.db_manager.users_collection.find_one({"username": username})

        #Verify the correctness of the credentials entered
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return {"error": "Invalid credentials"}, 401

        #JWT token generation
        access_token = create_access_token(identity={"username": username})
        return {"access_token": access_token}, 200

#Initializing the DatabaseManager
db_manager = DatabaseManager()

#Initializing the User Class
users = User(db_manager)

#Route for registering a new user
@app.route('/register', methods=['POST'])
def register():
    #Gets JSON data sent from the frontend
    data = request.json
    name = data.get('name')
    surname = data.get('surname')
    fiscal_code = data.get('fiscal_code')
    date_of_birth = data.get('date_of_birth')
    username = data.get('username')
    password = data.get('password')
#Calling the registration method of the User class
    response, status = users.registration(name, surname, fiscal_code, date_of_birth, username, password)
    return jsonify(response), status #Return HTTP response and status

#Route for user login
@app.route('/login', methods=['POST'])
def login():
    #Gets JSON data sent from the frontend
    data = request.json
    username = data.get('username')
    password = data.get('password')
#Calling the User Class login method
    response, status = users.login(username, password)
    return jsonify(response), status #Return HTTP response and status

#Secure route that requires JWT authentication
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity() #Retrieve the user's identity from the JWT token
    return jsonify({"message": f"Welcome {current_user['username']}!"}), 200 #Personalized welcome message
# Launch the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True) #Debug mode enabled
