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

invalid_password_response = {
    "password": ["Password must have a number and a letter"]
}

correct_user_details = {
    "username": "username1",
    "password": "pass1234",
    "email": "email@username1.com",
}


def update_pass(new_pass):
    details = correct_user_details.copy()
    details["password"] = new_pass
    return details


long_password_user_data = update_pass("P1" * 75)

invalid_password_user_data = update_pass("Platyrhyn")

long_password_user_data_response = {
    "password": ["Password cannot be more than 128 characters"]
}

correct_user_details_response = {
    "message": "Please confirm your Quexl account by clicking on the link "
    "sent to your email account %s" % correct_user_details.get("email")
}

details_without_email = {"password": "pass123", "username": "username2"}

details_without_username = {"password": "pass123", "email": "email@quexl.com"}

user_details_without_email_response = {"email": ["Please fill in the email."]}

user_details_without_username_response = {
    "username": ["Please fill in the username."]
}
