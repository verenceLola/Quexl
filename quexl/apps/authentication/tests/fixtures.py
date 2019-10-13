from quexl.apps.authentication.backends import JWTAuthentication

user_details_without_email = {
    "password": "pass123",
    "email": None,
    "username": "username2",
}

user_details_without_username = {
    "password": "pass123",
    "username": None,
    "email": "email@quexl.com",
}

correct_user_details = {
    "username": "username1",
    "password": "pass1234",
    "email": "email@username1.com",
}

correct_user_details_response = {
    "message": "Please confirm your Quexl account by clicking on the link "
    "sent to your email account %s" % correct_user_details.get("email"),
    "data": {
        "username": "%s" % correct_user_details.get("username"),
        "email": "%s" % correct_user_details.get("email"),
    },
}

details_without_email = {"password": "pass123", "username": "username2"}

details_without_username = {"password": "pass123", "email": "email@quexl.com"}

user_details_without_email_response = {"email": ["Please fill in the email."]}

user_details_without_username_response = {
    "username": ["Please fill in the username."]
}

existing_username_response = {
    "response": {
        "username": ["The username already exists. Kindly try another."]
    }
}

existing_email_response = {
    "response": {"email": ["Email address already exists"]}
}

invalid_password_response = {
    "password": ["Password must have a number and a letter"]
}


def update_pass(new_pass):
    details = correct_user_details.copy()
    details["password"] = new_pass
    return details


invalid_password_user_data = update_pass("Platyrhyn")
long_password_user_data = update_pass("P1" * 75)

long_password_user_data_response = {
    "password": ["Password cannot be more than 128 characters"]
}

signup_user_GET_response = {
    "response": {"message": "Only POST requests are allowed to this endpoint."}
}

correct_login_details = {"password": "pass123", "email": "user1@quexl.com"}

correct_login_response = "You have successfully logged in"


def update_login_details(detail, value):
    """
    update login details
    """
    new_login = correct_login_details.copy()
    if value is None:
        new_login.pop(detail)
    else:
        new_login[detail] = value
    return new_login


invalid_login_password = update_login_details("password", "worngPass1")
invalid_login_email = update_login_details("email", "wrong@email.com")
blank_password_login = update_login_details("password", "")
blank_email_login = update_login_details("email", "")
missing_email_login = update_login_details("email", None)
missing_password_login = update_login_details("password", None)
login_failed_response = {
    "error": [
        "Either your email or password isn’t right. Double check them, or"
        " reset your password to log in. "
    ]
}

blank_email_login_response = {"email": ["This field may not be blank."]}

missing_email_login_response = {"email": ["This field may not be null."]}

missing_password_login_response = {"password": ["This field may not be null."]}

blank_password_login_response = {"password": ["This field may not be blank."]}

valid_reset_token = JWTAuthentication().generate_reset_token("user1@quexl.com")

forgot_password_response = {
    "response": {
        "success": "An email has been sent to your inbox with a password reset link."
    }
}

reset_password_response = {
    "message": "Your password has been successfully changed",
    "data": {"email": "user1@quexl.com"},
}

reset_password_invalid_token_response = {
    "error": "Invalid token. Please request a new password reset link."
}
