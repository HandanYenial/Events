# Events
Events website is designed for searching for events in your area. It lets you to search for an event in any area by using a keyword and a city name, and add your favorite events to your personalized event list.

Ticketmaster Api is used for this project : https://app.ticketmaster.com/discovery/v2/

The website is deployed here: ...........................

## Pages and Usage
**Homepage:** Homepage displays random events in United States with event name,date,genre and event ticket sales information.It also enables users to add this event to their personal event list and reach ticketmaster website to purchase the event ticket.

**Events:** Events page allows user to search for an event with a keyword as music, baseball or community and a city name. Search results displays on the same page as cards with event information.

**Profile:** Displays user information, and user comments.

**Event List:** Display event list for the user. 

## Tech Stack
- ***Heroku*** :A container-based cloud Platform as a Service (PaaS)it is used to deploy and manage the website.

- ***Gunicorn:*** Python application for running multiple Python processes on Heroku.(The app is prepared on flask, with gunicorn we run it on heroku)

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
|    /signup     |Get/Post |      No          | Create and display a new user with SignUpForm built by WTForms with username,email,password,img_url(optional),first name and last name.|
|    /login      | Get/Post |      Yes         | Display the login form built by WTForms and authenticate the user.|
|    /logout     | Get| No| Logout the user and clear any information in the session|
|/ users/user_id| Get| Yes|Show user profile : username, user image, user comments and links to several pages|
|/users/edit|Get/Post|Yes|Edit profile for the user by using EditUserForm built ib WTForms|
|/users/delete|Post|Yes|Delete user|
|/homepage|Get|No|Displays random images around United States|
|/events|Get/Post|No|Search for events by keyword and city name by SearchForm (WTForms) and display results in cards designed with Bootstrap5, including event image, event name,event genre,family-friendly, ticket sales end date.|
|events/event_id/wishlist|Get/Post| Yes| Add events to user event list and display them on Event List page.Render event ids from Api and save them in the database.|
|/comments/new|Get/Post|Yes|Display comment form(WTForms) and add comment with username|
|/comments| Get| No|Show all comments in a table sorted by date posted.|
|/comments/comment_id/delete| Post |Yes|Enables user to delete the comment on webpage and on database.|

##Database Schema
![DatabaseDiagram](https://user-images.githubusercontent.com/88174651/169098721-13c7fc10-2897-4587-8c36-86def8db6e7d.png)





