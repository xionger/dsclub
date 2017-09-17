from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SelectMultipleField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

from app.models import Topic, Post, Forum, User, Report

class QuickreplyForm(FlaskForm):
	content = TextAreaField("Quick reply", 
		validators=[DataRequired("You cannot post a reply without content.")])

	submit = SubmitField("Reply")

	def save(self, user, topic):
		post = Post(content=self.content.data)
		return post.save(user=user, topic=topic)

class ReplyForm(FlaskForm):
	content = TextAreaField('Content', 
		validators=[DataRequired("You cannot post an empty content.")])

	track_topic = BooleanField('Track this topic', default=False, validators=[Optional()])

	submit = SubmitField('Reply')
	preview = SubmitField('Preview')

	def save(self, user, topic):
		post = Post(content=self.content.data)

		if self.track_topic.data:
			user.track_topic(topic)

		return post.save(user=user, topic=topic)

class NewTopicForm(ReplyForm):
	title = StringField('Topic title', 
		validators=[DataRequired("Please choose a title for your topic.")])

	content = TextAreaField('Content', 
		validators=[DataRequired('You cannot post an empty content.')])

	track_topic = BooleanField('Track this topic', default=False, validators=[Optional()])

	submit = SubmitField('Post Topic')
	preview = SubmitField('Preview')

	def save(self, user, forum):
		topic = Topic(title=self.title.data)
		post = Post(content=self.content.data)

		if self.track_topic.data:
			user.track_topic(topic)

		return topic.save(user=user, forum=forum, post=post)

class ReportForm(FlaskForm):
	reason = TextAreaField("Reason", 
		validators=[DataRequired("What is the reason for reporting this post?")])

	submit = SubmitField("Report post")

	def save(self, user, post):
		report = Report(reason=self.reason.data)
		return report.save(post=post, user=user)

