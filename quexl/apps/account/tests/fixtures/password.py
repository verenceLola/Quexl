from ...backends import JWTAuthentication

reset_password_response = {
    "message": "Your password has been successfully changed"
}

reset_password_invalid_token_response = {
    "error": "Invalid token. Please request a new password reset link."
}
valid_reset_token = JWTAuthentication().generate_reset_token("user1@quexl.com")
