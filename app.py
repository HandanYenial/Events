import os

from flask import Flask, render_template, redirect, flash, session, jsonify,request,g,abort
#from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from dateutil import parser

from models import db, connect_db, User, Comment, Wishlist, bcrypt
from forms import SearchForm, CommentForm, SignUpForm, UserEditForm, LoginForm, DeleteForm, WishlistForm
import requests
import json

CURR_USER_KEY = "curr_user"

API_BASE_URL = 'https://app.ticketmaster.com/discovery/v2/events?apikey=1g89Fx2KHiAD3WdLaBFtpKdTxZEW2lvS'

app = Flask(__name__)
         
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///event_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = "secret1234"
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
connect_db(app)
#toolbar = DebugToolbarExtension(app)


########### API routes ################

@app.route("/" , methods = ["GET"]) 
def show_homepage():
    """Show homepage with events limit is 20"""
    
    events=[]
    #item = {"keyword":"rock"}
    my_event = requests.get(API_BASE_URL)
    the_event_info = my_event.json() #this is a dictionary
    #print(the_event_info['page']['totalElements'])

    if the_event_info['page']['totalElements'] != 0:
        for event in the_event_info['_embedded']['events']:
            event_dic = {}
            event_dic['name'] = event['name']
            event_dic['url'] = event['url']
            event_dic['dates'] = event['dates']
            event_dic['images'] = event['images'][2]['url']
            event_dic['images'] = event['images'][2]['url'] 
            event_dic['classifications']  = event['classifications'][0]
            event_dic['sales'] = event['sales']
            event_dic['id'] = event['id']
            py_date = parser.parse(event['sales']['public']['endDateTime'])
            event_dic['sales_end_date'] = py_date.strftime("%Y-%m-%d %H:%M")
          
            events.append(event_dic)

    return render_template("homepage.html" ,events=events, my_event=my_event,the_event_info=the_event_info)


@app.route('/events', methods=['GET','POST'])
def search():
    """Search for events by using a keyword and a city name"""
  
    form = SearchForm()
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
                py_date = parser.parse(event['sales']['public']['endDateTime'])
                event_dic['sales_end_date'] = py_date.strftime("%Y-%m-%d %H:%M")
                events.append(event_dic)
                
    return render_template("index.html" , form=form, events=events)
  
##############################################################################
#The before_request decorator allows us to create a function that will run before each request.
#before_request functions are ideal for tasks such as:
#1.openning database connections
#2.Loading user from the session 
#3.Working with the flask g object

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup' , methods = ['GET' , 'POST'])
def signup():
    """Create the new user with username, password,email,name and lastname and add to database"""
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = SignUpForm() #in the form.py

    if form.validate_on_submit(): #getting all the data from the form
        try:
            username = form.username.data
            email = form.email.data
            password = form.password.data
            img_url= form.img_url.data or User.img_url.default.arg,
            first_name = form.first_name.data
            last_name = form.last_name.data

            user = User.signup(username,email,password,img_url, first_name,last_name)
            db.session.commit()

        except IntegrityError as e:
            flash("This username is already taken, please choose another username." , "danger")
            return render_template('colorlib-regform-3/index.html' , form=form)

        do_login(user)

        return redirect(f"/users/{user.id}")
    else:
        return render_template('signup2.html' , form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/users/{user.id}")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logout the user
    Clear any information from the session"""
    
    session.pop('username' , None)

    flash("Log in to access your account", 'success')
    return redirect("/login")


######################  User Routes  ##############################

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user profile."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    
    comments = (Comment
                .query
                .filter(Comment.user_id == user_id)
                .order_by(Comment.timestamp.desc())
                .limit(100)
                .all())
    
    return render_template('details.html', user=user, comments=comments)


@app.route('/users/edit', methods=["GET", "POST"])
def edit_user():
    """Edit profile for current user."""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
        
    user = g.user
    form = UserEditForm(obj=user)   

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.img_url = form.img_url.data or User.img_url.default.arg,

            db.session.commit()
            return redirect(f"/users/{user.id}")

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

    events = []
    search_items = {'id' : event_id} 
    result = requests.get(API_BASE_URL, params=search_items)
    the_event_info = result.json() 

    for event in the_event_info['_embedded']['events']:
        event_dic = {}
        event_dic['name'] = event['name']
        event_dic['url'] = event['url']
        # event_dic['dates'] = event['dates']
        event_dic['images'] = event['images'][2]['url'] 
    
        events.append(event_dic)
        entry = Wishlist(
                user_id = g.user.id,
                event_id = json.dumps(event['id']),
                event_name = json.dumps(event['name']),
                event_url = json.dumps(event['url']),
               # event_date = json.dumps(event['dates']),
                event_image = json.dumps(event['images'][2]['url']))

        db.session.add(entry)
        db.session.commit()

        return render_template("wishlist.html" , form=form , events=events, the_event_info=the_event_info )


## We have a got a dictionary with same columns/props of models
## We need to save that to the db

#################### Comments Routes #########################

@app.route('/comments/new', methods=["GET", "POST"])
def add_comment():
    """Add a comment"""
    print("*******")
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = CommentForm()

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

    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(comment)
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

       
