from flask import flash, redirect, render_template, url_for, request
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user

from . import forum
from app.models import Forum

from .forms import NewTopicForm

from app.utils.helper import register_view
from app.utils.setting import app_settings

"""
@forum.route('/forum/career')
def forum_career():
	return render_template('forum/show_forum.html', title="Careers")

@forum.route('/forum/data_analysis')
def forum_data_analysis():
	return render_template('forum/show_forum.html', title="Data Analysis")

@forum.route('/forum/data_mining')
def forum_data_mining():
	return render_template('forum/show_forum.html', title="Data Mining")

@forum.route('/forum/data_visualization')
def forum_data_visualization():
	return render_template('forum/show_forum.html', title="Data Visualization")

@forum.route('/forum/machine_learning')
def forum_machine_learning():
	return render_template('forum/show_forum.html', title="Machine Learning")

@forum.route('/forum/probability_statistics')
def forum_probability_statistics():
	return render_template('forum/show_forum.html', title="Probability and Statistics")

@forum.route('/forum/programming')
def forum_programming():
	return render_template('forum/show_forum.html', title="Programming")

@forum.route('/forum/resource')
def forum_resource():
	return render_template('forum/show_forum.html', title="Resources")

"""
class ViewForum(MethodView):

	def get(self, forum_id, slug=None):
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

register_view(forum, 
	routes=['/forum/<int:forum_id>'], view_func=ViewForum.as_view('view_forum'))

register_view(forum,
    routes=['/<int:forum_id>/topic/new'], view_func=NewTopic.as_view('new_topic'))
