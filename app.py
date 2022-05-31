import os

from flask import Flask, render_template, redirect, flash, session, jsonify,request,g,abort
#import flask methods
#from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError #for errors in SQLAlchemy 
from werkzeug.exceptions import Unauthorized
from dateutil import parser #for date and time

from models import db, connect_db, User, Comment, Wishlist, bcrypt #Models used
from forms import SearchForm, CommentForm, SignUpForm, UserEditForm, LoginForm, DeleteForm #forms (WTForms)
import requests # is a library for making HTTP requests to API
import json #to add json support 

CURR_USER_KEY = "curr_user"

API_BASE_URL = 'https://app.ticketmaster.com/discovery/v2/events?apikey=1g89Fx2KHiAD3WdLaBFtpKdTxZEW2lvS'

app = Flask(__name__)
         
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URI' , 'postgresql://uodhbjdiqxodpu:b8793068e4f2eefc7040deff773cfdb31b157fee3f15e0f9417ca64c0a4be5e4@ec2-3-234-131-8.compute-1.amazonaws.com:5432/dd0o0h0h8goh08'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY' , 'secret1234')
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
connect_db(app)
#toolbar = DebugToolbarExtension(app)



##############################################################################
#The before_request decorator allows us to create a function that will run before each request.
#before_request functions are ideal for tasks such as:
#1.openning database connections
#2.Loading user from the session 
#3.Working with the flask g object

@app.before_request
def add_user_to_g():
    """ Will run before each request and if the user is logged in, it will add current user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY]) #if the current user is in the session then set user as global user.

    else:
        g.user = None #if the current user is not in session then set global user to none.

def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id #user's id will be same as the user's id in the session

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY] # logout the user by clearing the session

########### API routes ################

@app.route("/" , methods = ["GET"]) 
def show_homepage():
    """Show homepage with random events rendered from API"""
    
    events=[] # having an empty array, will push the results in this array
    my_event = requests.get(API_BASE_URL) # request data from API
    the_event_info = my_event.json() # and convert into a json file(this is a dictionary)
    
    if the_event_info['page']['totalElements'] != 0:         # if the result is not0-if there is a result of the request
        for event in the_event_info['_embedded']['events']:  #the API was an embedded API to reach each componentget through [_embedded][events]
            event_dic = {}                    #set an empty dictionary to add the API data(data is in json format so dic is used)
            event_dic['name'] = event['name'] #get data from API and put into the dictionary
            event_dic['url'] = event['url']
            event_dic['dates'] = event['dates']
            event_dic['images'] = event['images'][2]['url']
            event_dic['images'] = event['images'][2]['url'] 
            event_dic['classifications']  = event['classifications'][0]
            event_dic['sales'] = event['sales']
            event_dic['id'] = event['id']
            event_dic['venue'] = event['_embedded']['venues'][0]
            py_date = parser.parse(event['sales']['public']['endDateTime'])
            event_dic['sales_end_date'] = py_date.strftime("%Y-%m-%d %H:%M")
          
            events.append(event_dic) 

    return render_template("homepage.html" ,events=events, my_event=my_event,the_event_info=the_event_info)


@app.route('/events', methods=['GET','POST'])
def search():
    """Search for events by using a keyword and a city name"""
  
    form = SearchForm() #from WTforms
    events = []
    if form.validate_on_submit():
        text = form.text.data
        e_city = form.e_city.data 
        search_items = {'keyword' : text , 'city':e_city} 
        result = requests.get(API_BASE_URL, params=search_items)
        the_event_info = result.json() # dictionary
        #print(the_event_info['page']['totalElements'])

        if the_event_info['page']['totalElements'] != 0:
           
            for event in the_event_info['_embedded']['events']:
                event_dic = {}
                event_dic['name'] = event['name']
                event_dic['url'] = event['url']
                event_dic['dates'] = event['dates']
                event_dic['images'] = event['images'][2]['url'] 
                event_dic['classifications']  = event['classifications'][0]
                event_dic['id'] = event['id']
                event_dic['venue'] = event['_embedded']['venues'][0]
                py_date = parser.parse(event['sales']['public']['endDateTime'])
                event_dic['sales_end_date'] = py_date.strftime("%Y-%m-%d %H:%M")
                events.append(event_dic)
                
    return render_template("index.html" , form=form, events=events)
  

@app.route('/signup' , methods = ['GET' , 'POST'])
def signup():
    """Create the new user with username, password,email,name and lastname and add to database.
       Redirect user to user profile page.
       If there is already a user with the same username then flash message."""
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = SignUpForm() #WTforms

    if form.validate_on_submit(): #getting all the data from the form and validate
        try:
            username = form.username.data
            email = form.email.data
            password = form.password.data
            img_url= form.img_url.data or User.img_url.default.arg,
            first_name = form.first_name.data
            last_name = form.last_name.data

            user = User.signup(username,email,password,img_url, first_name,last_name) #calls the classmethod in Users class
            db.session.commit()

        except IntegrityError as e:
            flash("This username is already taken, please choose another username." , "danger")
            return render_template('signup2.html' , form=form)

        do_login(user)

        return redirect(f"/users/{user.id}") #user profile page
    else:
        return render_template('signup2.html' , form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Login user with username and password.
       Redirect user to profile page."""

    form = LoginForm() #use the login form- WTForms

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data) #authenticate the user - classmethod from Users class
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/users/{user.id}") #user redirected to profile page

        flash("Invalid credentials.", 'danger') #if the authentication is not successful then flash the message
                                                
    return render_template('login.html', form=form) 


@app.route('/logout')
def logout():
    """Logout the user
    Clear any information from the session"""
    
    do_logout()

    flash("Log in to access your account", 'success')
    return redirect("/login")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user profile."""

    if not g.user: #if user is not logged in then flash message and redirect user to homepage
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id) #get the user from database with user.id
    
    comments = (Comment
                .query
                .filter(Comment.user_id == user_id)
                .order_by(Comment.timestamp.desc())
                .limit(100)
                .all()) #show user's comments
    
    return render_template('details.html', user=user, comments=comments)


@app.route('/users/edit', methods=["GET", "POST"])
def edit_user():
    """Edit profile for current user."""
    
    if not g.user: #user needs to be logged in to edit the profile
        flash("Access unauthorized.", "danger")
        return redirect("/")
        
    user = g.user
    form = UserEditForm(obj=user)   #use the UserEditForm-WTF 

    if form.validate_on_submit():  #to validate the form the authentication should be successful.
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.img_url = form.img_url.data or User.img_url.default.arg,

            db.session.commit() #commit the changes
            return redirect(f"/users/{user.id}") #redirect user to profile page after editing the profile

        flash("Wrong password, please try again.", 'danger')

    return render_template('edit.html', form=form , user=user)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup") 

################### Events-Wishlist Routes ################

@app.route('/events/<event_id>/wishlist', methods=["GET" , "POST"])
def show_user_wishlist(event_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    result = requests.get(f'https://app.ticketmaster.com/discovery/v2/events/{event_id}?apikey=1g89Fx2KHiAD3WdLaBFtpKdTxZEW2lvS')
    event = result.json()

    entry = Wishlist(
            user_id = g.user.id,
            event_id = event['id'],
            event_name = event['name'],
            event_url = event['url'],
            # event_date = json.dumps(event['dates']),
            event_image = event['images'][2]['url'])

    db.session.add(entry)
    db.session.commit()

    user_wishlists = Wishlist.query.all()

    #for w in user_wishlists:
       # print(w.event_name)

    return render_template("wishlist.html", wishlist=user_wishlists )


@app.route('/events/<event_id>/delete', methods=["POST"])
def delete_event(event_id):
    """Delete a comment."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
                                               
    w_event = Wishlist.query.get_or_404(event_id)  #retrieve the event by event_id

 
    db.session.delete(w_event) #delete the event from database
    db.session.commit()

    return redirect(f"/users/{g.user.id}")


## We have a got a dictionary with same columns/props of models
## We need to save that to the db

#################### Comments Routes #########################

@app.route('/comments/new', methods=["GET", "POST"])
def add_comment():
    """Add a comment"""
    # print("*******") #to debug the routes using print
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = CommentForm() #using form from forms.py

    if form.validate_on_submit(): 
        comment = Comment(text=form.text.data,
                          eventname = form.eventname.data,
                          city= form.city.data)

        g.user.comments.append(comment)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('comments/new_comment.html', form=form)


@app.route('/comments')
def show_all_comments():
    """Show all comments sorted by the dates"""

    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    return render_template('comments/show_comments.html' , comments=comments)



@app.route('/comments/<int:comment_id>/delete', methods=["POST"])
def delete_comment(comment_id):
    """Delete a comment."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    comment = Comment.query.get_or_404(comment_id) #retrieve the comment by comment_id

    if comment.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(comment) #delete the comment from database
    db.session.commit()

    return redirect(f"/users/{g.user.id}")


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

 
def mapWishListObj(user_id, raw_event):
    wishlist = {}
    event = raw_event['_embedded']['events'][0]
    wishlist['user_id'] = user_id
    wishlist['event_name'] = event['name']
    wishlist['event_url'] = event['url']
    wishlist['event_date'] = event['dates']
    wishlist['event_image'] = event['images'][2]['url'] 
    # wishlist['classifications']  = event['classifications'][0]
    wishlist['event_id'] = event['id']  
    return wishlist 

       
