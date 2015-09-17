""" Module for email related functionality. """

from flask_mail import Message

import api

mail = None

from api.common import check, validate, safe_fail, WebException
from voluptuous import Required, Length, Schema
from datetime import datetime

password_reset_request_schema = Schema({
    Required('username'): check(
        ("Usernames must be between 3 and 20 characters.", [str, Length(min=3, max=20)]),
    )
})

password_reset_schema = Schema({
    Required("token"): check(
        ("This does not look like a valid token.", [str, Length(max=100)])
    ),
    Required('password'): check(
        ("Passwords must be between 3 and 20 characters.", [str, Length(min=3, max=20)])
    )
})

def reset_password(token_value, password, confirm_password):
    """
    Perform the password update operation.

    Gets a token and new password from a submitted form, if the token is found in a team object in the database
    the new password is hashed and set, the token is then removed and an appropriate response is returned.

    Args:
        token_value: the password reset token
        password: the password to set
        confirm_password: the same password again
    """

    validate(password_reset_schema, {"token": token_value, "password": password})
    user = api.user.find_user_by_token("password_reset", token_value)
    api.user.update_password_request({
            "new-password": password,
            "new-password-confirmation": confirm_password
    }, uid=user['uid'])

    api.user.delete_token(user['uid'], "password_reset")

def request_password_reset(username):
    """
    Emails a user a link to reset their password.

    Checks that a username was submitted to the function and grabs the relevant team info from the db.
    Generates a secure token and inserts it into the team's document as 'password_reset_token'.
    A link is emailed to the registered email address with the random token in the url.  The user can go to this
    link to submit a new password, if the token submitted with the new password matches the db token the password
    is hashed and updated in the db.

    Args:
        username: the username of the account
    """
    validate(password_reset_request_schema, {"username":username})
    user = safe_fail(api.user.get_user, name=username)
    if user is None:
        raise WebException("No registration found for '{}'.".format(username))

    token_value = api.user.set_token(user['uid'], "password_reset")

    body = """We recently received a request to reset the password for the following {0} account:\n\n\t{2}\n\nOur records show that this is the email address used to register the above account.  If you did not request to reset the password for the above account then you need not take any further steps.  If you did request the password reset please follow the link below to set your new password. \n\n {1}/reset#{3} \n\n Best of luck! \n\n ~The {0} Team
    """.format(api.config.competition_name, api.config.competition_urls[0], username, token_value)

    subject = "{} Password Reset".format(api.config.competition_name)

    message = Message(body=body, recipients=[user['email']], subject=subject)
    mail.send(message)

def send_user_verification_email(username):
    """
    Emails the user a link to verify his account. If email_verification is
    enabled in the config then the user won't be able to login until this step is completed.
    """

    user = api.user.get_user(name=username)

    token_value = api.user.set_token(user["uid"], "email_verification")

    #Is there a better way to do this without dragging url_for + app_context into it?
    verification_link = "{}/api/user/verify?uid={}&token={}".\
        format(api.config.competition_urls[0], user["uid"], token_value)

    body = """Verification link: {}""".format(verification_link)
    subject = "{} Account Verification".format(api.config.competition_name)

    message = Message(body=body, recipients=[user['email']], subject=subject)
    mail.send(message)
