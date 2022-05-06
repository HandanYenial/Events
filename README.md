# Events
Capstone Project 1 : An event search engine built by using Python, Flask, Wtforms,PostgreSQL and Jinja
Capstone Project Proposal

This website’s goal is to allow user to search for events taking place in a particular location, date and time.
The target demographic of this website is people who wants to enjoy some time by attending an event.

Ticketmaster Api will be used for pulling up information about a specific event such as date, 
time and location of the event or a specific area that user provides.

The database scheme will consists of:
a. Users with their username, password and email information.
b. Events with name,type,location,dates,images and information.
c. Image of each event(relation with events)
d. Favorite comments
e. Comment for events

User will sign up with a Username, password and email. The user will later login and reach their account. 
Once they are logged in, they can click on the event to favorite(wish list) and can see these favorite events in their user account. 
User will be able to add it to their Google calendar by a link provided, also add a comment for a specific event. 
