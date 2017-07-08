from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), index=True, unique=True)
	username = db.Column(db.String(60), index=True, unique=True)
	firstname = db.Column(db.String(60), index=True)
	lastname = db.Column(db.String(60), index=True)
	password_hash = db.Column(db.String(128))
	is_admin = db.Column(db.Boolean, default=False)

	#score = db.Column(db.Integer, default=100)

	"""
	Other columns with foreign keys: events, resources, projects, roles
	"""

	@property
	def password(self):
		raise AttributeError("Password is not readable.")

	@password.setter
	def password(self, password):
		"""
		Set password to hash a hashed password
		"""
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User: {}>'.format(self.username)

#Set up user loader
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class Resource(object):
	"""
	Post information in the resource page
	columns: id, author, content, time, likes
	"""
	def __init__(self, arg):
		pass

class Project (object):
	"""
	Stores the information about project
	columns: id, leader, content, timeline, participant, status, etc
	"""
	def __init__(self, arg):
		pass

class Event (object):
	"""
	Stores the information about event
	columns: id, host, content, time, (place), participant, status, etc 
	"""
	def __init__(self, arg):
		pass

class Comment(object):
	"""
	Stores comments of resources
	Columns: id, author, content, time, article_id(fk)
	"""
	def __init__(self, arg):
		pass
		
class Role(object):
	"""
	Admin levels of users
	values include admin, project leader, event host, etc
	"""
	def __init__(self, arg):
		pass
		