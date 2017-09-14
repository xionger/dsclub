from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SelectMultipleField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

from app.models import Topic, Post, Forum, User

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

