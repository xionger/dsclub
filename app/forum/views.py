import math
from datetime import datetime
from flask import flash, redirect, render_template, url_for, request
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user

from . import forum
from app.models import Forum, User, Topic, Post

from .forms import NewTopicForm, ReplyForm, QuickreplyForm, ReportForm

from app.utils.helper import register_view, real
from app.utils.setting import app_settings


class ViewForum(MethodView):

	def get(self, forum_id):
		page = request.args.get('page', 1, type=int)

		#forum_instance = Forum.get_forum(forum_id=forum_id)
		forum_instance = Forum.query.filter_by(id=forum_id).first_or_404()

		#if forum_instance.external:
		#	return redirect(forum_instance.external)

		topics = Forum.get_topics(
			forum_id=forum_instance.id, 
			page=page, 
			per_page=app_settings['topics_per_page'])

		return render_template('forum/show_forum.html', 
			forum=forum_instance, 
			topics=topics)

class ViewPost(MethodView):

	def get(self, post_id):
		post = Post.query.filter_by(id=post_id).first_or_404()
		post_in_topic = Post.query.filter(Post.topic_id == post.topic_id, 
			Post.id <= post_id).order_by(Post.id.asc()).count()
		page = math.ceil(post_in_topic / float(app_settings['posts_per_page']))

		return redirect(url_for('forum.view_topic', 
			topic_id=post.topic.id,
			page=page, 
			_anchor='pid{}'.format(post.id)))

class ViewTopic(MethodView):

	def get(self, topic_id, slug=None):
		page = request.args.get('page', 1, type=int)

		# Fetch some information about the topic
		#topic = Topic.get_topic(topic_id=topic_id, user=real(current_user))
		topic = Topic.query.filter_by(id=topic_id).first_or_404()

		# Count the topic views
		topic.views_count += 1
		topic.save()

		# fetch the posts in the topic
		posts = Post.query.\
		outerjoin(User, Post.user_id == User.id).\
		filter(Post.topic_id == topic.id).\
		add_entity(User).\
		order_by(Post.id.asc()).\
		paginate(page, app_settings['posts_per_page'], False)

		# Abort if there are no posts on this page
		if len(posts.items) == 0:
			abort(404)

		return render_template('forum/topic.html', 
			topic=topic, posts=posts, form=self.form())

	#@allows.requires(CanPostReply)
	def post(self, topic_id, slug=None):
		topic = Topic.get_topic(topic_id=topic_id, user=real(current_user))
		form = self.form()

		if not form:
			flash(_('Cannot post reply'), 'warning')
			return redirect('forum.view_topic', topic_id=topic_id, slug=slug)

		elif form.validate_on_submit():
			post = form.save(real(current_user), topic)
			return redirect(url_for('forum.view_post', post_id=post.id))

		else:
			for e in form.errors.get('content', []):
				flash(e, 'danger')

			return redirect(url_for('forum.view_topic', topic_id=topic_id))

	def form(self):

		#if Permission(CanPostReply):
		#	return QuickreplyForm()
		#return None
		return QuickreplyForm()

class NewTopic(MethodView):
	decorators = [login_required]
	form = NewTopicForm

	def get(self, forum_id, slug=None):
		forum_instance = Forum.query.filter_by(id=forum_id).first_or_404()
		return render_template('forum/new_topic.html', forum=forum_instance, form=self.form())

	def post(self, forum_id, slug=None):
		forum_instance = Forum.query.filter_by(id=forum_id).first_or_404()
		form = self.form()
		if 'preview' in request.form and form.validate():
			return render_template('forum/new_topic.html', 
				forum=forum_instance, form=form, preview=form.content.data)

		elif 'submit' in request.form and form.validate():
			topic = form.save(real(current_user), forum_instance)
			# redirect to the new topic
			return redirect(url_for('forum.view_topic', topic_id=topic.id))

		else:
			return render_template('forum/new_topic.html', forum=forum_instance, form=form)

class NewPost(MethodView):
	decorators = [login_required]
	form = ReplyForm

	def get(self, topic_id, slug=None):
		topic = Topic.query.filter_by(id=topic_id).first_or_404()
		return render_template('forum/new_post.html', topic=topic, form=self.form())

	def post(self, topic_id, slug=None):
		topic = Topic.query.filter_by(id=topic_id).first_or_404()
		form = self.form()
		if form.validate_on_submit():
			if 'preview' in request.form:
				return render_template('forum/new_post.html', 
					topic=topic, form=form, preview=form.content.data)

			else:
				post = form.save(real(current_user), topic)
				return redirect(url_for('forum.view_post', post_id=post.id))

		return render_template('forum/new_post.html', topic=topic, form=form)

class ReplyPost(MethodView):
	decorators = [login_required]
	form = ReplyForm

	def get(self, topic_id, post_id):
		topic = Topic.query.filter_by(id=topic_id).first_or_404()
		return render_template('forum/new_post.html', topic=topic, form=self.form())

	def post(self, topic_id, post_id):
		form = self.form()
		topic = Topic.query.filter_by(id=topic_id).first_or_404()
		if form.validate_on_submit():
			if 'preview' in request.form:
				return render_template('forum/new_post.html', 
					topic=topic, form=form, preview=form.content.data)

			else:
				post = form.save(real(current_user), topic)
				return redirect(url_for('forum.view_post', post_id=post.id))

		else:
			form.content.data = format_quote(post.username, post.content)

		return render_template('forum/new_post.html', topic=post.topic, form=form)

class EditPost(MethodView):
	decorators = [login_required]
	form = ReplyForm

	def get(self, post_id):
		post = Post.query.filter_by(id=post_id).first_or_404()
		form = self.form(obj=post)
		return render_template('forum/new_post.html', topic=post.topic, form=form, edit_mode=True)

	def post(self, post_id):
		post = Post.query.filter_by(id=post_id).first_or_404()
		form = self.form(obj=post)

		if form.validate_on_submit():
			if 'preview' in request.form:
				return render_template('forum/new_post.html', 
					topic=post.topic, 
					form=form, 
					preview=form.content.data, 
					edit_mode=True)

			else:
				form.populate_obj(post)
				post.date_modified = datetime.now()
				post.modified_by = real(current_user).username
				post.save()
				return redirect(url_for('forum.view_post', post_id=post.id))

		return render_template('forum/new_post.html', topic=post.topic, form=form, edit_mode=True)

class DeleteTopic(MethodView):
	decorators = [login_required]

	def post(self, topic_id, slug=None):
		topic = Topic.query.filter_by(id=topic_id).first_or_404()
		involved_users = User.query.filter(Post.topic_id == topic.id, User.id == Post.user_id).all()
		topic.delete(users=involved_users)

		return redirect(url_for('forum.view_forum', forum_id=topic.forum_id))

class DeletePost(MethodView):
	decorators = [login_required]

	def post(self, post_id):
		post = Post.query.filter_by(id=post_id).first_or_404()
		first_post = post.first_post
		topicUrl = post.topic.url
		forumUrl = post.topic.forum.url

		post.delete()

		# If the post was the first post in the topic, redirect to the forums
		if first_post:
			return redirect(forumUrl)

		return redirect(topicUrl)

class ReportView(MethodView):
	decorators = [login_required]
	form = ReportForm

	def get(self, post_id):
		return render_template('forum/report_post.html', form=self.form())

	def post(self, post_id):
		form = self.form()

		if form.validate_on_submit():
			post = Post.query.filter_by(id=post_id).first_or_404()
			form.save(real(current_user), post)
			flash('Thanks for reporting.', 'success')

		return render_template('forum/report_post.html', form=form)


register_view(forum, 
	routes=['/forum/<int:forum_id>'], view_func=ViewForum.as_view('view_forum'))

register_view(forum, 
	routes=['/post/<int:post_id>'], view_func=ViewPost.as_view('view_post'))

register_view(forum, 
	routes=['/topic/<int:topic_id>/post/<int:post_id>/reply'], view_func=ReplyPost.as_view('reply_post'))

register_view(forum, 
	routes=['/post/<int:post_id>/delete'], view_func=DeletePost.as_view('delete_post'))

register_view(forum, 
	routes=['/post/<int:post_id>/edit'], view_func=EditPost.as_view('edit_post'))

register_view(forum,
    routes=['/<int:forum_id>/topic/new'], view_func=NewTopic.as_view('new_topic'))

register_view(forum, 
	routes=['/topic/<int:topic_id>'], view_func=ViewTopic.as_view('view_topic'))

register_view(forum, 
	routes=['/topic/<int:topic_id>/delete'], view_func=DeleteTopic.as_view('delete_topic'))

register_view(forum, 
	routes=['/post/<int:post_id>/report'], view_func=ReportView.as_view('report_post'))
