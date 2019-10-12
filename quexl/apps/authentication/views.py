import datetime
import furl
import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from rest_framework.response import Response
from quexl.apps.authentication.email import send_email
from quexl.apps.authentication.backends import JWTAuthentication
from quexl.helpers.endpoint_response import get_success_responses
from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, ResetPasswordSerializer,
    ForgotPasswordSerializer, UserSerializer

)


class RegistrationAPIView(GenericAPIView):
    """Register a new user"""
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request, **kwargs):
        """ Signup a new user """
        email, username, password = request.data.get(
            'email', None), request.data.get(
            'username', None), request.data.get('password', None)

        user = {"email": email, "username": username, "password": password}

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        send_email(request, user)
        serializer.save()

        response_data = {
            "username": username,
            "email": email
        }

        return get_success_responses(
            data=response_data,
            message="Please confirm your Quexl account by clicking on the "
                    "link sent to your email account {}".format(email),
            status_code=status.HTTP_201_CREATED
        )

    def get(self, request):
        return Response(
            data={
                "message": 'Only POST requests are allowed to this endpoint.'
            })


class UserActivationAPIView(GenericAPIView):
    """Activate a user after mail verification."""
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def get(self, request, token, *args, **kwargs):
        """ Method for getting user token and activating them. """
        # After a successful registration, a user is activated through here
        # The token that was created and sent is decoded to get the user
        # The user's is_active attribute is then set to true
        try:
            data = JWTAuthentication.decode_jwt(token)
            user = User.objects.get(username=data['userdata'])
        except:  # noqa
            return Response(
                data={"message": "Activation link is invalid."},
                status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response(
            data={
                "message": "Account activated successfully."
            },
            status=status.HTTP_200_OK
        )


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        """Login a user"""
        email, password = request.data.get('email', None), request.data.get(
            'password', None)

        user = {"email": email, "password": password}
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data

        user = User.get_user(user_data['email'])
        userdata = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        user_data['token'] = \
            JWTAuthentication.generate_token(userdata=userdata)

        return get_success_responses(
            data=user_data,
            message="You have successfully logged in",
            status_code=status.HTTP_200_OK
        )

    def get(self):
        """Get a user"""
        return Response(
            data={
                "message": 'Only post requests are allowed to this endpoint.'
            })


class ForgotPasswordView(GenericAPIView):
    # This view handles sending the password reset request email.
    # We expect the user to enter an email that exists in the database
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        """User Forgot Password"""
        try:
            requester_data = request.data.get('email')
            user = User.objects.get(email=requester_data)

            # Get URL for client and include in the email for password reset
            subject = "Password Reset - Quexl"
            message = 'Reset your password '

            # generate token token that expires afteer 24 hours
            token = jwt.encode({
                "email": user.email,
                "iat": datetime.datetime.now(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(
                    hours=24)
            }, settings.SECRET_KEY, algorithm='HS256').decode()

            # format url and send it in the reset email link

            # TODO: Configure link to refer upon password reset
            client_url = request.META.get(
                'HTTP_REFERER', request.build_absolute_uri('/').strip("/")
            )
            reset_link_url = furl.furl(client_url)
            reset_link_url.args = (('token', token),)

            body = render_to_string('reset_password.html', {
                'link': reset_link_url,
                'name': user.username
            })

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                html_message=body,
                fail_silently=True
            )
            return Response({
                "success": "An email has been sent to your inbox with a "
                            "password reset link."},
                            status=status.HTTP_200_OK)

        except (KeyError, User.DoesNotExist):
            return Response({
                "error": "Missing or non-existing email."},
                status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(GenericAPIView):
    # This is the view that changes the password.
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def put(self, request, token, *args, **kwargs):
        try:
            new_password = request.data.get('password')
            serializer = self.serializer_class(data={"password": new_password})
            serializer.is_valid(raise_exception=True)
            decode_token = jwt.decode(token, settings.SECRET_KEY,
                                      algorithms="HS256")
            email = decode_token.get('email')
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return get_success_responses(
                message="Your password has been successfully changed",
                data={
                    "email": email
                },
                status_code=status.HTTP_200_OK
            )
        except jwt.PyJWTError:
            return Response({
                "error": "Invalid token. Please request a new password reset "
                         "link."},
                status=status.HTTP_403_FORBIDDEN)


class UserResourceAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, user_id, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        try:
            user = User.get_user_by_id(user_id=user_id)
            userdata = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "image": user.photo,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
            return get_success_responses(
                data=userdata,
                message="User details fetched successfully",
                status_code=status.HTTP_200_OK
            )

        except (KeyError, User.DoesNotExist):
            return Response({
                "error": "That user id does not exist."},
                status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),

            'profile': {
                'photo': user_data.get('photo', request.user.profile.photo),
                'bio': user_data.get('bio', request.user.profile.bio),
                'country': user_data.get('country',
                                         request.user.profile.country),
                'phone': user_data.get('phone', request.user.profile.phone),
            }
        }

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        updated_fields = dict()
        for k, v in user_data.items():
            if k in serializer_data['profile']:
                updated_fields.update({k: v})

        data = {
            "message": "Update successful",
            "updated-fields": updated_fields,
            "new-record": serializer_data
        }

        return get_success_responses(
            data=data,
            message="User profile successfully updated",
            status_code=status.HTTP_200_OK
        )
