from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from rest_framework import status
from core_module.models import Profile, User
from django.contrib.auth.signals import user_logged_out
from custom_exception_message import CustomAPIException
from custom_decorator import response_modify_decorator_post, \
        response_modify_decorator_get_after_execution, \
        response_modify_decorator_update, \
        response_decorator_list_or_get_after_execution_onoff_pagination, \
        response_modify_decorator_get_single_after_execution
from users.knox_views.views import LoginView as KnoxLoginView, LogoutAllView
from users.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.exceptions import APIException
from datetime import datetime
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from core_module.utils import generate_token


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(
            redirect_url,
            'Thank you for your email confirmation. \
            Now you can login your account.'
            )
    else:
        return redirect(expired_redirect_url)



class CreateUserView(generics.CreateAPIView):
    """Create a new user in system"""
    permission_classes = [AllowAny]
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @response_modify_decorator_post
    def post(self, request, format=None):
        data = {}
        with transaction.atomic():
            user_exist = self.queryset.filter(
                email=request.data['email']).exists()
            if not user_exist:
                raise CustomAPIException(
                    None,
                    'You Have Entered An Invalid Email Address',
                    status_code=status.HTTP_400_BAD_REQUEST)
            user_is_active = self.queryset.filter(
                email=request.data['email'],
                is_active=True)
            if not user_is_active:
                raise APIException(
                    None,
                    "sorry, Account is not active !",
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            response = super(LoginView, self).post(request, format=None)
            user_detials = self.queryset.get(email=user)
            user_detials.last_login = datetime.now()
            user_detials.save()
            profile_query = Profile.objects.filter(user=user)
            if profile_query:
                first_name = profile_query.get().firstname
                data['message'] = f'Hello {first_name}, Welcome Back!'
            data['token'] = response.data['token']
            data['token_expiry'] = response.data['expiry']
            data['user_details'] = {
                        "user_id": user_detials.id,
                        "name": user_detials.name,
                        "email": user_detials.email,
            }
            return Response(data)



