# Events
<img src = "https://user-images.githubusercontent.com/88174651/169122261-646682bc-e95e-44f0-b165-974fe9978c08.gif"  width="250" height="250" />



The Events web app is specifically designed to help users search for events in a particular area. By simply entering a keyword and a city name, users can easily find events that match their interests. Additionally, users have the option to add their favorite events to a personalized event list for easy reference later on.

Ticketmaster Api is used for this project: https://app.ticketmaster.com/discovery/v2/

The website is deployed here: https://events2022.herokuapp.com/

## Pages and Usage
**Homepage:** Homepage displays random events in the United States with event names, dates, genres, and event ticket sales information. It also enables users to add this event to their personal event list and reach the Ticketmaster website to purchase the event ticket.

**Events:** The Events page enables users to search for specific events using keywords such as music, baseball, or community, along with a city name. The search results are displayed on the same page in the form of cards, each containing information about a particular event.

**Profile:** Displays user information and user comments.

**Event List:** Display the event list for the user. 

## Tech Stack
- ***Heroku***:A container-based cloud Platform as a Service (PaaS) is used to deploy and manage the website.

- ***Gunicorn:*** Python application for running multiple Python processes on Heroku. (The app is prepared on Flask, with gunicorn we run it on Heroku)

- ***Flask:***  A Python web framework with useful tools and features.

- ***Jinja:*** A web template engine for the Python programming language, used for creating dynamic html files.

- ***SQLAlchemy:*** A library to obtain communication between Python programs and databases. It is used as an ORM(Objact Relational Mapper).

- ***WTForms:*** A python library that privides web form rendering and data validation.

- ***PostgreSQL:*** Database, primary data storage.

- ***Bcrypt:*** To hash the user passwords. 

- ***HTML5:*** A markup language to structure and present content on website.

- ***CSS:*** To style the webpage

- ***Font Awesome:*** An icon set used for scalable vector images.

- ***Bootstrap5:*** To create a responsive webpage.

## How is the Ticketmaster Api used in Events?
**Event Search**
__Method:__ GET

__Summary:__ Event Search

__Description:__ Find events and filter your search by location, date, availability, and much more.

__/discovery/v2/events__

__Query Parameters:__
|   Parameter      |    Description                                            |    Type    |
-------------------|-----------------------------------------------------------|--------------|
|     id           | Filter entities by its id                                 |    String    |
|   keyword        | Keyword to search on                                      |    String    |
| startDateTime    | Filter with a start date after this date                  |    String    |
|onsaleEndDateTime | Filter with onsale end date before this date              |    String    |
|      city        | Filter by city                                            |    Array     |
|classificationName| Filter by classification name: name of any segment, genre,sub-genre, type, sub-type.|     Array    |
                     
## Events Routes 
|     Routes     |  Method  |  Login Required  |          Details             |
|----------------|----------|------------------|------------------------------|
|    /signup     |Get/Post |      No          | Create and display a new user with SignUpForm built by WTForms with username, email, password,img_url(optional), first name, and last name.|
|    /login      | Get/Post |      Yes         | Display the login form built by WTForms and authenticate the user.|
|    /logout     | Get| No| Logout the user and clear any information in the session|
|/ users/user_id| Get| Yes|Show user profile: username, user image, user comments, and links to several pages|
|/users/edit|Get/Post|Yes|Edit profile for the user by using EditUserForm built ib WTForms|
|/users/delete|Post|Yes|Delete user|
|/homepage|Get|No|Displays random images around United States|
|/events|Get/Post|No|Search for events by keyword and city name by SearchForm (WTForms) and display results in cards designed with Bootstrap5, including event image, event name, event genre, family-friendly, and ticket sales end date.|
|events/event_id/wishlist|Get/Post| Yes| Add events to the user event list and display them on the Event List page. Render event ids from Api and save them in the database.|
|/comments/new|Get/Post|Yes|Display comment form(WTForms) and add comment with username|
|/comments| Get| No|Show all comments in a table sorted by the date posted.|
|/comments/comment_id/delete| Post |Yes|Enables user to delete the comment on the webpage and on the database.|

## Database Schema
![DatabaseDiagram](https://user-images.githubusercontent.com/88174651/169098721-13c7fc10-2897-4587-8c36-86def8db6e7d.png)





