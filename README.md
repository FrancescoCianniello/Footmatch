Footmatch
Footmatch is a web app designed to help users search for tickets to football events. It offers a wide choice of matches involving Italian teams involved in Serie A and European competitions (Champions League, Europa League and Conference League).                                                                In this way, the user can find the tickets of his favorite team in a very simple way and can buy them through an equally simple payment method.                                                                                        To access the app you must be registered and then log in with the username and password provided during registration. If the login is successful, the user accesses the home page from which he can use all the functions. There are icons to access personal information, purchase, search for tickets only to obtain information (without buying) and to the icons are added a button for logout and a menu that summarizes all the functions and allows access to a document explaining the web app and ticket reservations.                                                                     The home page also shows the tickets for the next ten matches in chronological order.          The search is performed through filters that concern the name of the team, the date of the match and the number of the round of the competition (to these is also added the name of the competition when the search is general and not specific).                                                                        As for the technologies used, Python and Flask were used for the backend while HTML5, Javascript and CSS were used for the frontend.The JQuery library was used for the animations while the data management took place through a MongoDB database. All this to provide the user with a user-friendly web app that allows him to go to the stadium to support his favorite team without having to wait for the immense queues of the box office or having to move with difficulty in apps that show more options and more events.Below is a description of each individual file within the project:

app.py: Implementation of the server in Python using the Flask microframework to handle http requests from different domains (Flask-CORS). The server manages a ticket sales system for football matches and also provides a registration and login system based on JWT authentication with the use of bcrypt to hide passwords by hashing them.

script.js: Implementation in JavaScript to manage registration, login, page security and logout. In addition, through the JQuery library, an animation is implemented to bounce the logo, in order to simulate the behavior of a ball.

style.css: Used to describe the styling of application elements.

aboutus.html: HTML document that describes in general what Footmatch is and provides information on how to use the app and what competitions are available.

account.html: HTML code for managing the display of the user profile, retrieving the information entered during registration from the MongoDB database (except the password).

championsleague.html: This HTML code creates a dynamic page to display Champions League matches, with search functionality based on criteria such as team, date, and round.

europaleague.html: This HTML code creates a dynamic page to display Europa League matches, with search functionality based on criteria such as team, date and round.

conferenceleague.html: This HTML code creates a dynamic page to display Conference League matches, with search functionality based on criteria such as team, date, and round.

serieA.html: This HTML code creates a dynamic page to display Serie A matches, with search functionality based on criteria such as team, date, and round.

findcompetition.html: Simple and intuitive interface to select the competition for which you want to have information regarding tickets.

login.html: Login page where you must fill out a form by entering the username and password indicated during registration.

registration.html: Registration page where the data must be entered in a form that represents the first step to be taken in order to use the app.

webapp.html: home page of the app that shows the next ten matches and from which you can access all the features present through icons or menu.

welcome.html: Html page used to simply show a welcome message to the user after successful login.

mybookings.html: Interface to display user bookings retrieved from the backend and regarding purchases made by the user.

payment.html: Implementation of a form for the management of payments after choosing the ticket and indicating its quantity.

purchase.html: Implementation of the purchase through a search by filters (competition, team, date and round) and updating both the total price based on the selected quantity and the number of tickets available after purchase.

Simulation of use
User Francesco Bianchi plans to buy three tickets to go to the Venezia-Inter match on 12 January 2025 and decides to try the new Footmatch web app. The first step is to register in order to be recognized later by the system. Francesco enters his data and memorizes his username and password that he will need later in the login phase. Just registered, start the login process by clicking on the link below the registration. At this point, log in by entering your username and password and, if everything is successful, the user has access to the home page of the web app. From here it is possible to find information on the next ten matches for which it is possible to purchase and access all the features both from icons and from specific links in the menu. The user can view the information related to the app in the "About us" section, see the information entered during registration in the "My account" section, access their reservations in "My bookings", and can use two other sections which are "Competitions" and "Purchase". The first can be used to obtain information on scheduled matches through a filter search by choosing the desired competition. The "Purchase" section, on the other hand, is related to purchases and allows you to search for the desired ticket through the filters and to be able to select the quantity requested, before being able to access the section dedicated to payment where the actual purchase is made official. Francesco must then access the "Purchase" section in order to reach his goal and search for the ticket by choosing the competition, team name, match date and round number. Once you have found your ticket, you must select three as the quantity and click on the buy button. This opens the section dedicated to payments where you enter your data, so you can easily and quickly buy tickets. At this point, the available tickets are automatically updated while those booked by Francesco are entered in the "My bookings" section. Just the goal has been reached, the user can close the app by clicking on the logout button.
