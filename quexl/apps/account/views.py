import datetime
import furl
import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from django.utils.timezone import now
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from quexl.apps.account.email import send_email
from quexl.apps.account.backends import JWTAuthentication
from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    UserSerializer,
    SocialAuthSerializer,
    MeSerializer,
)
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import MissingBackend
from social_django.utils import load_strategy, load_backend


class RegistrationAPIView(GenericAPIView):
    """Register a new user"""

    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer
    operation = "Signup"

    def post(self, request, **kwargs):
        """ Signup a new user """
        email, username, password = (
            request.data.get("email", None),
            request.data.get("username", None),
            request.data.get("password", None),
        )

        user = {"email": email, "username": username, "password": password}

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        send_email(request, user)
        serializer.save()

        return Response(
            {
                "message": "Please confirm your Quexl account by clicking on the "
                "link sent to your email account {}".format(email)
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        return Response(
            {"message": "Only POST requests are allowed to this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class UserActivationAPIView(GenericAPIView):
    """Activate a user after mail verification."""

    permission_classes = (AllowAny,)
    operation = "Account activation"

    def get(self, request, token, *args, **kwargs):
        """ Method for getting user token and activating them. """
        # After a successful registration, a user is activated through here
        # The token that was created and sent is decoded to get the user
        # The user's is_active attribute is then set to true
        try:
            data = JWTAuthentication.decode_jwt(token)
            user = User.objects.get(username=data["userdata"])
        except (User.DoesNotExist, jwt.exceptions.DecodeError):
            return Response(
                {"message": "Activation link is invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = True
        user.save()
        return Response(
            {"message": "Account activated successfully."},
            status=status.HTTP_200_OK,
        )


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    operation = "Login"
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        """Login a user"""
        email, password = (
            request.data.get("email", None),
            request.data.get("password", None),
        )

        user = {"email": email, "password": password}
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        # if not serializer.is_valid():
        #     return Response({
        #         'errors': serializer.errors
        #     })
        user_data = serializer.data

        user = User.get_user(user_data["email"])
        userdata = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }
        token = JWTAuthentication.generate_token(userdata=userdata)
        # update user last login
        user.last_login = now()
        user.save()
        return Response(
            {"message": "You have successfully logged in", "token": token},
            status=status.HTTP_200_OK,
        )


class ForgotPasswordView(GenericAPIView):
    # This view handles sending the password reset request email.
    # We expect the user to enter an email that exists in the database
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        """User Forgot Password"""
        try:
            requester_data = request.data.get("email")
            user = User.objects.get(email=requester_data)

            # Get URL for client and include in the email for password reset
            subject = "Password Reset - Quexl"
            message = "Reset your password "

            # generate token token that expires after 24 hours
            token = jwt.encode(
                {
                    "email": user.email,
                    "iat": datetime.datetime.now(),
                    "exp": datetime.datetime.utcnow()
                    + datetime.timedelta(hours=24),
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            ).decode()

            # format url and send it in the reset email link

            # TODO: Configure link to referer upon password reset
            client_url = request.META.get(
                "HTTP_REFERER", request.build_absolute_uri("/").strip("/")
            )
            reset_link_url = furl.furl(client_url)
            reset_link_url.args = (("token", token),)

            body = render_to_string(
                "reset_password.html",
                {"link": reset_link_url, "name": user.username},
            )

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                html_message=body,
                fail_silently=True,
            )
            return Response(
                {
                    "message": "An email has been sent to your inbox with a "
                    "password reset link."
                },
                status=status.HTTP_200_OK,
            )

        except (KeyError, User.DoesNotExist):
            return Response(
                {
                    "message": "Password Reset Request failed",
                    "error": "Missing or non-existing email.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class ResetPasswordView(GenericAPIView):
    # This is the view that changes the password.
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer
    operation = "Password reset"

    def put(self, request, token, *args, **kwargs):
        try:
            new_password = request.data.get("password")
            serializer = self.serializer_class(data={"password": new_password})
            serializer.is_valid(raise_exception=True)
            decode_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
            email = decode_token.get("email")
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Your password has been successfully changed"},
                status=status.HTTP_200_OK,
            )
        except jwt.PyJWTError:
            return Response(
                {
                    "error": "Invalid token. Please request a new password reset "
                    "link."
                },
                status=status.HTTP_403_FORBIDDEN,
            )


class UserResourceAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, user_id, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        self.operation = "View user details"
        try:
            user = User.get_user_by_id(user_id=user_id)
            userdata = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
            return Response(
                {
                    "message": "User details fetched successfully",
                    "details": userdata,
                },
                status=status.HTTP_200_OK,
            )

        except (KeyError, User.DoesNotExist, AttributeError):
            return Response(
                {
                    "message": "Failed to fetch user details",
                    "error": "That user id %s does not exist." % user_id,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, *args, **kwargs):
        new_data = request.data
        self.operation = "Update user details"  # set operation name
        serializer = self.serializer_class(
            request.user, data=new_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_fields = dict()
        for k, v in new_data.items():
            updated_fields.update({k: v})

        return Response(
            {
                "message": "User details successfully updated",
                "updated-fields": updated_fields,
                "new-record": new_data,
            },
            status=status.HTTP_200_OK,
        )


class SocialAuthView(GenericAPIView):
    """Authenticate via social sites (Google & Facebook)"""

    permission_classes = (AllowAny,)
    serializer_class = SocialAuthSerializer
    operation = "Social authentication"

    def post(self, request, *args, **kwargs):
        """Takes in provider and access_token to authenticate user"""
        serializer = self.serializer_class(data=request.data["authData"])
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get("provider")
        authenticated_user = (
            request.user if not request.user.is_anonymous else None
        )  # noqa E501
        strategy = load_strategy(request)

        # Load backend associated with the provider
        try:
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None
            )
            if isinstance(backend, BaseOAuth1):
                if "access_token_secret" in request.data:
                    access_token = {
                        "oauth_token": request.data["access_token"],
                        "oauth_token_secret": request.data[
                            "access_token_secret"
                        ],  # noqa E501
                    }
                else:
                    return Response(
                        {"error": "Access token secret is required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            elif isinstance(backend, BaseOAuth2):

                access_token = serializer.data.get("access_token")

        except MissingBackend:
            return Response(
                {"error": "The Provider is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Go through the pipeline to create user if they don't exist
        try:
            user = backend.do_auth(access_token, user=authenticated_user)
            user.is_active = True
            user.save()

        except BaseException:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        if user and user.is_active:
            userdata = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
            token = JWTAuthentication.generate_token(userdata=userdata)

            return Response(
                {
                    "message": "You have successfully logged in.",
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )


class AuthMeRetriveAPIView(RetrieveAPIView):
    """
    return the current user info
    """

    renderer_classes = (UserJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    serializer_class = MeSerializer

    def get_object(self):
        """
        retrive current user info
        """
        email = self.request.user.email
        return User.objects.get(email=email)
