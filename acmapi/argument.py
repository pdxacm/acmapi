from flask.ext.restful import abort
from flask.ext.restful.reqparse import Argument

class CustomArgument(Argument):

    def handle_validation_error(self, error):
        
        msg = self.help if self.help is not None else str(error)
        abort(400, message=msg, exception=error.__class__.__name__)
