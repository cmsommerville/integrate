from flask_restx import Resource
from app.tasks.email import send_email


class TestResource(Resource):
    def post(self, *args, **kwargs):
        try:
            message_dict = {
                "from_email": "Chandler Sommerville <donotreply@sommerville.dev>",
                "to_emails": "cmsommerville@gmail.com",
                "subject": "It's been a while!",
                "html_content": "<strong>This is a test email</strong>",
            }
            send_email.delay(message_dict)
        except Exception as e:
            return {"error": str(e)}, 500
        else:
            return {"status": "Success"}, 200
