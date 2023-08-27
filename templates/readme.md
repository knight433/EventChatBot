# Chatbot Integration
___

The Chatbot is created using Javascript, Jquery for functionality and Python Flask as backend. For styling Bootstrap is used along with pure CSS.

Flask_socketio is used as websockets for seamless communication between the user and the bot.

To run this, make sure flask, flask_socketio are installed. This is also specified in the **requirements.txt** file.

When the website has loaded the button can be seen in the bottom right corner of the screen. 
The window that rolls up after the button press is made as responsive as possible. Bootstrap wasn't used here. 

In the html page the div with the class **'stays'** is where you add your content to the website.

html page is located in **'/chatApp/templates'** folder <br/>
css page is in **'/chatApp/static'** folder

# Changes  made in reply.py file. 
___
- The functions which were printing the output to the console are made to return the output instead.
- The while loop is removed from the reply function and the ***run*** segment is removed.
- Small changes here and there.



# Python files
___
- on.py: This file creates the flask app and integrates the socketio into it.
- events.py: Handles the asynchronous communication between the bot and the user.
- extensions.py: Simply an extension to create the socketio object.
- routes.py: Where the routes of the website are defines. Can be used to create api calls here.
