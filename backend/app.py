#Importation of the necessary libraries
from flask import Flask, request, jsonify #Backend
from flask_cors import CORS #Cross-Origin requests as a security measure
from pymongo import MongoClient #Use of the database
import bcrypt #Password hash library
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity #For the use of JWT as an authentication system
import datetime


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
        self.users_collection = self.db['users']  #Collections creation
        self.tickets_collection=self.db['tickets']
        self.purchases_collection = self.db['purchases']

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

#Method for account information
@app.route('/account', methods=['GET'])
@jwt_required()  #  Requires a JWT token for authentication
def get_account():
    current_user = get_jwt_identity() # Gets the user's identity from the JWT token

    if not current_user:    # Check if the user exists in the token
        return jsonify({"error": "User not found"}), 404

    user = db_manager.users_collection.find_one({"username": current_user["username"]})  #Retrieve user data from the database using their username

    if user:
        user_data = {                 #Setting up user data
            "name": user.get("name"),
            "surname": user.get("surname"),
            "fiscal_code": user.get("fiscal_code"),
            "date_of_birth": user.get("date_of_birth"),
            "username": user.get("username")
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "User not found in database"}), 404

#Secure route that requires JWT authentication
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity() #Retrieve the user's identity from the JWT token
    return jsonify({"message": f"Welcome {current_user['username']}!"}), 200 #Personalized welcome message

#Ticket class to represent tickets
class Ticket:
    def __init__(self, database_manager):
        self.db_manager = database_manager             #Initialize the database manager

db_manager = DatabaseManager()

#Initializing the Ticket Class
tickets2= Ticket(db_manager)

#Method of getting tickets
@app.route('/tickets', methods=['GET'])
@jwt_required()  # Requires JWT authentication
def get_tickets():
    tickets = db_manager.tickets_collection.find()  #Gets all tickets from the database
    ticket_list = []    # List to store tickets

    for ticket in tickets:
        ticket_data = {        #Set up ticket details
            'id': ticket['_id'],
            'date': ticket['date'],
            'city': ticket['city'],
            'stadium': ticket['stadium'],
            'sales_start_date': ticket['sales_start_date'],
            'sales_end_date': ticket['sales_end_date'],
            'available_tickets': ticket['available_tickets'],
            'nationality_team1': ticket['nationality_team1'],
            'nationality_team2': ticket['nationality_team2'],
            'team1': ticket['team1'],
            'team2': ticket['team2'],
            'price':ticket['price'],
            'competition':ticket['competition'],
            'round':ticket['round'],
        }
        ticket_list.append(ticket_data)

    return jsonify(ticket_list), 200     #Returns the list of tickets

#class used to define the purchase
class Purchase:
    def __init__(self, database_manager):
        self.db_manager = database_manager      # Initialize the database manager

db_manager = DatabaseManager()

#Initializing the Purchase Class
purchases2= Purchase(db_manager)

#Method for defining ticket purchase
@app.route('/purchase', methods=['POST'])
@jwt_required()  # Requires JWT authentication
def purchase_ticket():
    data = request.json      #Gets the JSON data sent in the request
    ticket_id = data.get('ticket_id')
    quantity = data.get('quantity')
    cardholder = data.get('cardholder')
    card_number = data.get('card_number')
    expiry_month = data.get('expiry_month')
    expiry_year = data.get('expiry_year')
    cvv = data.get('cvv')

    # Please ensure that all the data is present
    if not all([cardholder, card_number, expiry_month, expiry_year, cvv]):
        return jsonify({"error": "Payment details are incomplete"}), 400    # Error response if payment details are incomplete

    # Retrieve ticket from the database
    ticket = db_manager.tickets_collection.find_one({"_id": ticket_id})
    if not ticket or ticket['available_tickets'] < quantity:
        return jsonify({"error": "Tickets unavailable"}), 400

    # Updating ticket availability
    new_available_tickets = ticket['available_tickets'] - quantity
    db_manager.tickets_collection.update_one(
        {"_id": ticket_id},
        {"$set": {"available_tickets": new_available_tickets}}
    )

#Card number masking to ensure security
    masked_card_number = card_number[-4:]

    # Inserts purchase details into the database
    db_manager.purchases_collection.insert_one({
        "user": get_jwt_identity(),  # Retrieve the user from the JWT token
        "ticket_id": ticket_id,
        "quantity": quantity,
        "purchase_date": datetime.datetime.now(),  # Date and time of purchase
        "cardholder": cardholder,
        "masked_card_number": masked_card_number,
        "expiry_month": expiry_month,
        "expiry_year": expiry_year
    })
    return jsonify({"message": "Purchase successful"}), 200

#Method for viewing purchases
@app.route('/my_bookings', methods=['GET'])
@jwt_required()  # Requires JWT authentication
def my_bookings():
    # Get the current user from the JWT token
    current_user = get_jwt_identity()
    purchases = db_manager.purchases_collection.find({"user": current_user})  # Gets the user's bookings from the database
    bookings = []     #List to store bookings

    for purchase in purchases:
        ticket = db_manager.tickets_collection.find_one({"_id": purchase['ticket_id']})   # Retrieve ticket details for each purchase

        if ticket:
            booking_data = {       #Set up booking details
                'ticket_id': purchase['ticket_id'],
                'quantity': purchase['quantity'],
                'purchase_date': purchase['purchase_date'],
                'ticket_details': {
                    'team1': ticket['team1'],
                    'team2': ticket['team2'],
                    'stadium': ticket['stadium'],
                    'competition': ticket['competition'],
                    'price': ticket['price'],
                    'date': ticket['date'],
                }
            }
            bookings.append(booking_data)   #Adds the data of each reservation to the list

    # Return the user's bookings data
    return jsonify(bookings), 200

# Launch the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True) #Debug mode enabled

