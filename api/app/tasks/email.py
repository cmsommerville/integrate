import os
import datetime
from celery import shared_task
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.extensions import db
from app.auth.models import Model_AuthUser


def send_email(message_dict):
    try:
        message = Mail(**message_dict)
        sg = SendGridAPIClient(os.getenv("EMAIL_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        return e


@shared_task()
def check_password_expired():
    dt = datetime.datetime.now() - datetime.timedelta(minutes=1)
    users_with_expired_pws = (
        db.session.query(Model_AuthUser)
        .filter(Model_AuthUser.password_last_changed_dt < dt)
        .all()
    )
    if users_with_expired_pws:
        users = ", ".join([user.user_name for user in users_with_expired_pws])
        message_dict = {
            "from_email": "Chandler Sommerville <donotreply@sommerville.dev>",
            "to_emails": "cmsommerville@gmail.com",
            "subject": "Expired passwords",
            "html_content": f"<h2>{users}</h2>",
        }
        send_email(message_dict)
