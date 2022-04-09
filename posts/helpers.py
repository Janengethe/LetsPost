#!/usr/bin/python3
"""
methods:
		logged_in -> returns True if user is logged in

"""

def logged_in(current_user):
	"""returns True if user is logged in"""
	try:
		_ = current_user.id
		return True
	except:
		return False