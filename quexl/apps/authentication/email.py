from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

from quexl.apps.authentication.backends import JWTAuthentication


def send_email(request, user):
    # sends email with the activation link with the token
    subject = 'Quexl Account Activation'
    message = 'Please verify your account '
    domain = get_current_site(request).domain
    token = JWTAuthentication.generate_token(user['username'])
    protocol = request.META['SERVER_PROTOCOL'][:4]
    activation_link = protocol + '://' + domain + '/api/auth/' + token
    body = render_to_string('verify_account.html', {
        'link': activation_link,
        'name': user['username']
    })

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user['email']],
            html_message=body,
        )
    except:  # noqa
        return Response(data={"message": "Email activation failed"},
                        status=status.HTTP_400_BAD_REQUEST)
