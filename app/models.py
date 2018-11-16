from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from flask_jwt import jwt, jwt_required, current_identity
# import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index=True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id=db.Column(db.Integer, db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash=db.Column(db.String(255))
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")
    comments=db.relationship('Comment', backref='user', lazy="dynamic")
    pitches = db.relationship('Pitch',backref='user',lazy='dynamic')
  

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash=generate_password_hash(password)

    def set_password(self,password):
        self.hash_pass = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users=db.relationship('User', backref='role', lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'



class Comment(db.Model):
    __tablename__='comments'

    id=db.Column(db.Integer, primary_key=True)
    time_posted = db.Column(db.DateTime,default=datetime.utcnow)
    comment_content=db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    opinion = db.Column(db.String(255))
    comment_id = db.Column(db.Integer)
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comments=Comment.query.order_by(Comment.time_posted.desc()).filter_by(pitches_id=id).all()
        return comments

class Votes(db.Model):
    __tablename__ = 'Votes'
    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))
    vote_number = db.Column(db.Integer)

    def save_Votes(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_votes(cls,user_id,pitch_id):
        interview = interveiw.query.filter_by(user_id=user_id,pitch_id=pitch_id).all()
        return votes

    @classmethod
    def num_vote(cls,pitch_id):
        found_votes = db.session.query(func.sum(Vote.vote_number))
        found_votes = found_votes.filter_by(pitch_id=pitch_id).group_by(Vote.pitch_id)
        votes_list = sum([i[0] for i in found_votes.all()])
        return votes_list



class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    pitch_content = db.Column(db.String())
    content = db.Column(db.String())
    pitch_category = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment = db.relationship("Comment", backref="pitches", lazy = "dynamic")
    vote = db.relationship("Vote", backref="pitches", lazy = "dynamic")

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitch(cls,id):
        pitches = Pitch.query.filter_by(id=id).all()
        return pitches

    @classmethod
    def get_pitches(cls, id):
        pitches = Pitch.query.order_by('-id').all()
        return pitches

    @classmethod
    def get_category(cls,cat):
        category = Pitch.query.filter_by(pitch_category=cat).order_by('-id').all()
        return category

