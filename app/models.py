import datetime
from datetime import timedelta
from pytz import UTC

from flask import url_for, abort
from flask_login import UserMixin

from sqlalchemy.orm import aliased
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

from app.utils.database import CRUDMixin, make_comparable

groups_users = db.Table(
	'groups_users',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False), 
	db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), nullable=False))

moderators = db.Table(
	'moderators', 
	db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), nullable=False),
	db.Column('forum_id', db.Integer(), db.ForeignKey('forums.id', 
		use_alter=True, name="ds_forum_id"), nullable=False))

topictracker = db.Table(
	'topictracker',
	db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), nullable=False), 
	db.Column('topic_id', db.Integer(), 
		db.ForeignKey('topics.id', use_alter=True, name="ds_tracker_topic_id"), nullable=False))

forumgroups = db.Table(
	'forumgroups', 
	db.Column('group_id', db.Integer(), db.ForeignKey('groups.id'), nullable=False), 
	db.Column('forum_id', db.Integer(), 
		db.ForeignKey('forums.id', use_alter=True, name="ds_forum_id"), nullable=False))

creators = db.Table(
	'creators', 
	db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), nullable=False),
	db.Column('project_id', db.Integer(), db.ForeignKey('projects.id', 
		use_alter=True, name="ds_project_id"), nullable=False))

participants = db.Table(
	'participants', 
	db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), nullable=False),
	db.Column('project_id', db.Integer(), db.ForeignKey('projects.id', 
		use_alter=True, name="ds_project_id"), nullable=False))

brainstormtracker = db.Table(
	'brainstormtracker',
	db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), nullable=False), 
	db.Column('brainstorm_id', db.Integer(), 
		db.ForeignKey('brainstorms.id', use_alter=True, name="ds_tracker_brainstorm_id"), nullable=False))

projectgroups = db.Table(
	'projectgroups', 
	db.Column('group_id', db.Integer(), db.ForeignKey('groups.id'), nullable=False), 
	db.Column('project_id', db.Integer(), 
		db.ForeignKey('prejects.id', use_alter=True, name="ds_project_id"), nullable=False))

class User(db.Model, UserMixin, CRUDMixin):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), index=True, unique=True, nullable=False)
	username = db.Column(db.String(64), index=True, unique=True, nullable=False)
	firstname = db.Column(db.String(64))
	lastname = db.Column(db.String(64))
	_password = db.Column('password', db.String(120), nullable=False)
	
	bio = db.Column(db.Text)
	occupation = db.Column(db.String(64))
	organization = db.Column(db.String(64))
	location = db.Column(db.String(128))
	avatar = db.Column(db.String(128))
	score = db.Column(db.Integer, default=0)
	profile_visible = db.Column(db.Integer, default=1)

	github = db.Column(db.String(255), nullable=True)
	linkedin = db.Column(db.String(255), nullable=True)
	kaggle = db.Column(db.String(255), nullable=True)
	
	date_joined = db.Column(db.DateTime, nullable=True)
	member_since = db.Column(db.DateTime, nullable=True)
	last_seen = db.Column(db.DateTime, nullable=True)

	last_failed_login = db.Column(db.DateTime, nullable=True)
	login_attempts = db.Column(db.Integer, default=0, nullable=False)
	activated = db.Column(db.Boolean, default=False, nullable=False)

	#is_member = db.Column(db.Boolean, default=False)
	#is_admin = db.Column(db.Boolean, default=False)
	#role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	posts = db.relationship('Post', backref='user', lazy='dynamic')
	topics = db.relationship("Topic", backref="user", lazy="dynamic")
	post_count = db.Column(db.Integer, default=0)

	discussions = db.relationship('Discussion', backref='user', lazy='dynamic')
	brainstorms = db.relationship('Brainstorm', backref='user', lazy='dynamic')
	disc_count = db.Column(db.Integer, default=0)

	primary_group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

	primary_group = db.relationship('Group', 
		lazy="joined", backref="user_group", uselist=False, foreign_keys=[primary_group_id])

	secondary_groups = db.relationship('Group', 
		secondary=groups_users, primaryjoin=(groups_users.c.user_id == id), 
		backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

	tracked_topics = db.relationship("Topic", 
		secondary=topictracker, primaryjoin=(topictracker.c.user_id == id), 
		backref=db.backref("topicstracked", lazy="dynamic"), lazy="dynamic")

	tracked_brainstorms = db.relationship("Brainstorm", 
		secondary=brainstormtracker, primaryjoin=(brainstormtracker.c.user_id == id), 
		backref=db.backref("brainstormstracked", lazy="dynamic"), lazy="dynamic")

	#projects = db.relationship('Project', backref='creator', lazy='dynamic')
	#projectParticipants = db.relationship('ProjectPaticipant', backref='participant', lazy='dynamic')

	#events = db.relationship('Event', backref='creator', lazy='dynamic')
	#eventParticipants = db.relationship('EventPaticipant', backref='participant', lazy='dynamic')

	#articles = db.relationship('Article', backref='author', lazy='dynamic')
	#brainstorms = db.relationship('Brainstorm', backref='author', lazy='dynamic')
	#discussions = db.relationship('Discussion', backref='author', lazy='dynamic')

	def _get_password(self):
		#Returns the hashed password.
		return self._password

	def _set_password(self, password):
		#Generates a password hash for the provided password.
		if not password:
			return 

		self._password = generate_password_hash(password)

	password = db.synonym('_password', descriptor=property(_get_password, _set_password))


	def check_password(self, password):
		#Check passwords. If passwords match it returns true, else false.
		if self.password is None:
			return False

		return check_password_hash(self.password, password)

	@property
	def url(self):
		#Returns the url for the user.
		return url_for("user.profile", username=self.username)

	@property
	def days_registered(self):
		#Returns the amount of days the user is registered.
		days_registered = (time_utcnow() - self.date_joined).days
		if not days_registered:
			return 1
		return days_registered

	@property
	def topic_count(self):
		#Returns the thread count.
		return Topic.query.filter(Topic.user_id == self.id).count()


	def __repr__(self):
		#Set to a unique key specific to the object in the database.
		#Required for cache.memoize() to work across requests.
		
		return "<{} {}>".format(self.__class__.__name__, self.username)

@make_comparable
class Group(db.Model, CRUDMixin):
	__tablename__ = "groups"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, nullable=False)
	description = db.Column(db.String(255), nullable=True)

	# Group types
	admin = db.Column(db.Boolean, default=False, nullable=False)
	super_mod = db.Column(db.Boolean, default=False, nullable=False)
	forum_mod = db.Column(db.Boolean, default=False, nullable=False)
	
	proj_creator = db.Column(db.Boolean, default=False, nullable=False)
	proj_part = db.Column(db.Boolean, default=False, nullable=False)

	member = db.Column(db.Boolean, default=True, nullable=False)
	fellow = db.Column(db.Boolean, default=False, nullable=False)
	banned = db.Column(db.Boolean, default=False, nullable=False)

	# Moderator permissions (only available when the user a moderator)
	mod_edituser = db.Column(db.Boolean, default=False, nullable=False)
	mod_banuser = db.Column(db.Boolean, default=False, nullable=False)
	mod_addscore = db.Column(db.Boolean, default=False, nullable=False)

	# User permissions
	editpost = db.Column(db.Boolean, default=True, nullable=False)
	deletepost = db.Column(db.Boolean, default=False, nullable=False)
	deletetopic = db.Column(db.Boolean, default=False, nullable=False)
	posttopic = db.Column(db.Boolean, default=True, nullable=False)
	postreply = db.Column(db.Boolean, default=True, nullable=False)

	# Methods
	def __repr__(self):
		#Set to a unique key specific to the object in the database.
		#Required for cache.memoize() to work across requests.
		
		return "<{} {} {}>".format(self.__class__.__name__, self.id, self.name)

	@classmethod
	def selectable_groups_choices(cls):
		return Group.query.order_by(Group.name.asc()).with_entities(Group.id, Group.name).all()

@make_comparable
class Forum(db.Model, CRUDMixin):
	__tablename__ = "forums"

	id = db.Column(db.Integer, primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
	title = db.Column(db.String(255), nullable=False)
	description = db.Column(db.Text, nullable=True)
	position = db.Column(db.Integer, default=1, nullable=False)
	locked = db.Column(db.Boolean, default=False, nullable=False)
	show_moderators = db.Column(db.Boolean, default=False, nullable=False)
	external = db.Column(db.String(255), nullable=True)
	post_count = db.Column(db.Integer, default=0, nullable=False)
	topic_count = db.Column(db.Integer, default=0, nullable=False)
	
	# One-to-one
	last_post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)
	last_post = db.relationship("Post", 
		backref="last_post_forum", uselist=False, foreign_keys=[last_post_id])

	last_post_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

	last_post_user = db.relationship("User", 
		uselist=False, foreign_keys=[last_post_user_id])

	#posts = db.relationship('Post', backref='forum', lazy='dynamic')

	# One-to-many
	topics = db.relationship("Topic", backref="forum", lazy="dynamic", cascade="all, delete-orphan")

	# Many-to-many
	moderators = db.relationship("User", 
		secondary=moderators, 
		primaryjoin=(moderators.c.forum_id == id),
		backref=db.backref("forummoderator", lazy="dynamic"), lazy="joined")

	groups = db.relationship(
		"Group", secondary=forumgroups, 
		primaryjoin=(forumgroups.c.forum_id == id), backref="forumgroups", lazy="joined")

	"""
	@property
	def slug(self):
		#Returns a slugified version from the forum title
		return slugify(self.title)

	@property
	def url(self):
		#Returns the slugified url for the forum
		if self.external:
		return self.external
		return url_for("forum.view_forum", forum_id=self.id, slug=self.slug)

	@property
	def last_post_url(self):
		#Returns the url for the last post in the forum
		return url_for("forum.view_post", post_id=self.last_post_id)
	"""

	def __repr__(self):
		"""Set to a unique key specific to the object in the database.
		Required for cache.memoize() to work across requests.
		"""
		return "<{} {}>".format(self.__class__.__name__, self.id)

@make_comparable
class Category(db.Model, CRUDMixin):
	__tablename__ = "categories"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	description = db.Column(db.Text, nullable=True)
	position = db.Column(db.Integer, default=1, nullable=False)

	# One-to-many
	forums = db.relationship("Forum", backref="category", lazy="dynamic", 
		primaryjoin='Forum.category_id == Category.id', order_by='asc(Forum.position)', 
		cascade="all, delete-orphan")

@make_comparable
class Topic(db.Model, CRUDMixin):
	__tablename__ = "topics"

	id = db.Column(db.Integer, primary_key=True)
	forum_id = db.Column(db.Integer, 
		db.ForeignKey("forums.id", use_alter=True, name="ds_topic_forum_id"), nullable=False)

	title = db.Column(db.String(255), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
	#username = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False)
	last_updated = db.Column(db.DateTime, nullable=False)
	locked = db.Column(db.Boolean, default=False, nullable=False)
	featured = db.Column(db.Boolean, default=False, nullable=False)

	views_count = db.Column(db.Integer, default=0, nullable=False)
	post_count = db.Column(db.Integer, default=0, nullable=False)

	# One-to-one (uselist=False) relationship between first_post and topic
	first_post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=True)
	first_post = db.relationship("Post", 
		backref="first_post", uselist=False, foreign_keys=[first_post_id])

	# One-to-one
	last_post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)
	last_post = db.relationship("Post", 
		backref="last_post", uselist=False, foreign_keys=[last_post_id])

	# One-to-many
	posts = db.relationship("Post", backref="topic", lazy="dynamic", 
		primaryjoin="Post.topic_id == Topic.id", cascade="all, delete-orphan", post_update=True)

@make_comparable
class Post(db.Model, CRUDMixin):
	__tablename__ = "posts"

	id = db.Column(db.Integer, primary_key=True)
	topic_id = db.Column(db.Integer, db.ForeignKey("topics.id", use_alter=True, 
		name="ds_post_topic_id", ondelete="CASCADE"), nullable=True)

	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
	#username = db.Column(db.String(200), nullable=False)
	content = db.Column(db.Text, nullable=False)
	attached = db.Column(db.String(255), nullable=True)
	
	date_created = db.Column(db.DateTime, nullable=False)
	date_modified = db.Column(db.DateTime, nullable=True)
	modified_by = db.Column(db.String(200), nullable=True)
	vote = db.Column(db.Integer, default=0)

	parent_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	parent = db.relationship("Post", remote_side=[id])


	def __repr__(self):
		"""Set to a unique key specific to the object in the database.
		Required for cache.memoize() to work across requests.
		"""
		return "<{} {}>".format(self.__class__.__name__, self.id)

@make_comparable
class Project(db.Model, CRUDMixin):
	__tablename__ = "projects"

	id = db.Column(db.Integer, primary_key=True)
	is_event = db.Column(db.Boolean, default=False)

	title = db.Column(db.String(255), nullable=False)
	tasks = db.Column(db.Text, nullable=False)
	where = db.Column(db.String(255))
	start = db.Column(db.DateTime, nullable=False)
	end = db.Column(db.DateTime, nullable=True)
	join_by = db.Column(db.DateTime, nullable=True)

	date_created = db.Column(db.DateTime, nullable=False)
	last_updated = db.Column(db.DateTime, nullable=False)
	position = db.Column(db.Integer, default=1, nullable=False)

	is_open = db.Column(db.Boolean, default=True)
	finished = db.Column(db.Boolean, default=False)
	locked = db.Column(db.Boolean, default=False, nullable=False)
	#show_creators = db.Column(db.Boolean, default=True, nullable=False)
	external = db.Column(db.String(200), nullable=True)

	# One-to-one
	last_discussion_id = db.Column(db.Integer, db.ForeignKey("discussions.id"), nullable=True)
	last_discussion = db.relationship("Discussion", 
		backref="last_discussion_project", uselist=False, foreign_keys=[last_discussion_id])

	last_discussion_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

	last_discussion_user = db.relationship("User", 
		uselist=False, foreign_keys=[last_discussion_user_id])

	# One-to-many
	brainstorms = db.relationship("Brainstorm", 
		backref="project", lazy="dynamic", cascade="all, delete-orphan")

	# Many-to-many
	creators = db.relationship("User", 
		secondary=creators, primaryjoin=(creators.c.project_id == id),
		backref=db.backref("projectcreator", lazy="dynamic"), lazy="joined")

	participants = db.relationship("User", 
		secondary=participants, 
		primaryjoin=(participants.c.project_id == id),
		backref=db.backref("projectprticipant", lazy="dynamic"), lazy="joined")

	groups = db.relationship(
		"Group", secondary=projectgroups,
		primaryjoin=(projectgroups.c.project_id == id), backref="projectgroups", lazy="joined")

	#creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	#paticipants = db.relationship('ProjectParticipant', backref='project', lazy='dynamic')

	#articles = db.relationship('Article', backref='project', lazy='dynamic')
	#brainstorms = db.relationship('Brainstorm', backref='project', lazy='dynamic')

@make_comparable
class Brainstorm(db.Model, CRUDMixin):
	__tablename__ = "brainstorms"

	id = db.Column(db.Integer, primary_key=True)
	project_id = db.Column(db.Integer, 
		db.ForeignKey("projects.id", use_alter=True, name="ds_brainstorm_project_id"), nullable=False)

	title = db.Column(db.String(255), nullable=False)
	is_article = db.Column(db.Boolean, default=False)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
	#username = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False)
	last_updated = db.Column(db.DateTime, nullable=False)
	locked = db.Column(db.Boolean, default=False, nullable=False)
	featured = db.Column(db.Boolean, default=False, nullable=False)

	views_count = db.Column(db.Integer, default=0, nullable=False)
	post_count = db.Column(db.Integer, default=0, nullable=False)

	# One-to-one (uselist=False) relationship between first_post and topic
	first_discussion_id = db.Column(db.Integer, 
		db.ForeignKey("discussions.id", ondelete="CASCADE"), nullable=True)
	first_discussion = db.relationship("Discussion", 
		backref="first_discussion", uselist=False, foreign_keys=[first_discussion_id])

	# One-to-one
	last_discussion_id = db.Column(db.Integer, db.ForeignKey("discussions.id"), nullable=True)
	last_discussion = db.relationship("Discussion", 
		backref="last_discussion", uselist=False, foreign_keys=[last_discussion_id])

	# One-to-many
	discussions = db.relationship("Discussion", 
		backref="brainstorm", lazy="dynamic", 
		primaryjoin="Discussion.brainstorm_id == Brainstorm.id", 
		cascade="all, delete-orphan", post_update=True)

@make_comparable
class Discussion(db.Model, CRUDMixin):
	__tablename__ = "discussions"

	id = db.Column(db.Integer, primary_key=True)
	brainstorm_id = db.Column(db.Integer, db.ForeignKey("brainstorms.id", use_alter=True, 
		name="ds_discussion_brainstorm_id", ondelete="CASCADE"), nullable=True)

	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
	#username = db.Column(db.String(200), nullable=False)
	content = db.Column(db.Text, nullable=False)
	attached = db.Column(db.String(255), nullable=True)
	
	date_created = db.Column(db.DateTime, nullable=False)
	date_modified = db.Column(db.DateTime, nullable=True)
	modified_by = db.Column(db.String(200), nullable=True)
	vote = db.Column(db.Integer, default=0)

	parent_id = db.Column(db.Integer, db.ForeignKey('discussions.id'))
	parent = db.relationship("Discussion", remote_side=[id])

	"""
	@property
	def url(self):
		#Returns the url for the post.
		return url_for("project.view_projpost", post_id=self.id)

	def __init__(self, content=None, user=None, brainstorm=None):
		#Creates a post object with some initial values.
		#:param content: The content of the post.
		#:param user: The user of the post.
		#:param topic: Can either be the topic_id or the topic object.
		
		if content:
			self.content = content

		if user:
			# setting user here -- even with setting the user id explicitly
			# breaks the bulk insert for some reason
			self.user_id = user.id
			self.username = user.username

		if brainstorm:
			self.brainstorm_id = brainstorm if isinstance(brainstorm, int) else brainstorm.id

		self.date_created = time_utcnow()
	"""

	def __repr__(self):
		"""Set to a unique key specific to the object in the database.
		Required for cache.memoize() to work across requests.
		"""
		return "<{} {}>".format(self.__class__.__name__, self.id)

class Conversation(db.Model, CRUDMixin):
	__tablename__ = "conversations"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
	to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
	#shared_id = db.Column(UUIDType, nullable=False)

	subject = db.Column(db.String(255), nullable=True)
	date_created = db.Column(db.DateTime, nullable=False)
	date_modified = db.Column(db.DateTime, nullable=False)
	trash = db.Column(db.Boolean, default=False, nullable=False)
	draft = db.Column(db.Boolean, default=False, nullable=False)
	unread = db.Column(db.Boolean, default=False, nullable=False)

	messages = db.relationship("Message", 
		lazy="joined", backref="conversation", 
		primaryjoin="Message.conversation_id == Conversation.id", 
		order_by="asc(Message.id)", cascade="all, delete-orphan")

	# this is actually the users message box
	user = db.relationship("User", lazy="joined", foreign_keys=[user_id])
	# the user to whom the conversation is addressed
	to_user = db.relationship("User", lazy="joined", foreign_keys=[to_user_id])
	# the user who sent the message
	from_user = db.relationship("User", lazy="joined", foreign_keys=[from_user_id])

class Message(db.Model, CRUDMixin):
	__tablename__ = "messages"

	id = db.Column(db.Integer, primary_key=True)
	conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)

	# the user who wrote the message
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	message = db.Column(db.Text, nullable=False)
	date_created = db.Column(db.DateTime, nullable=False)

	user = db.relationship("User", lazy="joined")