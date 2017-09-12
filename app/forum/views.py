from flask import render_template

from . import forum

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