from flask import render_template

from . import resource

@resource.route('/resources')
def show_resources():
	return render_template('resource/show_resources.html', title="Resources")