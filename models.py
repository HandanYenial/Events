from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

img = "https://media.istockphoto.com/vectors/upcoming-events-neon-signs-vector-upcoming-events-design-template-vector-id978975308?k=20&m=978975308&s=612x612&w=0&h=HnwHCKofUyVji7q4Vqpg9VI0avrWdF8hr-nA5EATfmk="
tba = "To be announced"
ATTRACTION_IMG = 'https://www.google.com/url?sa=i&url=http%3A%2F%2Fspiritgeek.com%2F2016%2F01%2Fcoming-attractions-for-2016.html&psig=AOvVaw2r-0IVfJWpU8uyd_hCgts6&ust=1651117007256000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCPiclq2os_cCFQAAAAAdAAAAABAI'
USER_ICON = "/static/images/emoji.png"


class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    username   = db.Column(db.String(20) , unique=True, nullable=False)
    password   = db.Column(db.String , nullable=False)
    email      = db.Column(db.String(50) , nullable=False , unique=True)
    first_name = db.Column(db.String(30) , nullable=False)
    last_name  = db.Column(db.String(30) , nullable = False)
    img_url    = db.Column(db.String , default = "/static/images/emoji.png")
    comments   = db.relationship('Comment', cascade ='all,delete' )
    wishlist   = db.relationship('Wishlist' , cascade ='all,delete' )
    

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, img_url, first_name,last_name):
        """Sign up user.
        Hashes password and adds the user to the system.
        """

        print("BEFORE HASH", password)
        hashed_pwd = bcrypt.generate_password_hash(password).decode("utf8")

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            img_url=img_url,
            first_name = first_name,
            last_name = last_name
   
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that the user exists & password is correct.
        Return user if valid; else return False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            #print("&&&&&")
            print(is_auth, user.password, password)
            if is_auth:
                return user

        return False

   
class Comment(db.Model):
    __tablename__ = "comments"
    
    id        = db.Column(db.Integer, primary_key=True,autoincrement=True ) 
    city      = db.Column(db.String , nullable = True)
    eventname = db.Column(db.String , nullable = True)
    text      = db.Column(db.String(200), nullable = False)
    timestamp = db.Column(db.DateTime , nullable=False , default=datetime.utcnow())
    user_id   = db.Column(db.Integer , db.ForeignKey('users.id')) 
        
    user = db.relationship('User')



class Wishlist(db.Model):
    __tablename__ = "wishlists"

    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.String)
    event_name = db.Column(db.String)
    event_url = db.Column(db.String)
   #  event_date = db.Column(db.DateTime , nullable=False , default=datetime.utcnow())
    event_image =db.Column(db.String)

   
def connect_db(app):
    db.app = app
    db.init_app(app)





