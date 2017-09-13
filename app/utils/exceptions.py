from werkzeug.exceptions import HTTPException, Forbidden


class DSclubError(HTTPException):

	description = "An internal error has occured"


class AuthorizationRequired(DSclubError, Forbidden):
	description = "Authorization is required to access this area."


class AuthenticationError(DSclubError):
	description = "Invalid username and password combination."