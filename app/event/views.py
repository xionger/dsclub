from flask import render_template
from flask_login import login_required

from . import event

@event.route('/events/coming')
def coming_events():
	return render_template('event/coming_events.html', title="Coming Events")

@event.route('/events/past')
def past_events():
	return render_template('event/past_events.html', title="Past Events")

@event.route('/events/create')
#@login_required
def create_event():
	return render_template('event/create_event.html', title="Create Event")