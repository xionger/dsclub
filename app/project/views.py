from flask import render_template
from flask_login import login_required

from . import project

@project.route('/projects/ongoing')
def ongoing_projects():
	return render_template('project/ongoing_projects.html', title="Ongoing Projects")

@project.route('/projects/completed')
def completed_projects():
	return render_template('project/completed_projects.html', title="Completed Projects")

@project.route('/projects/create')
#@login_required
def create_project():
	return render_template('project/create_project.html', title="Create Project")