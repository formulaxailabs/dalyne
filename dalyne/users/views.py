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
# from custom_functions import get_client_ip
# from custom_exception_message import CustomAPIException
# from custom_decorator import response_modify_decorator_post, \
#         response_modify_decorator_get_after_execution, \
#         response_modify_decorator_update, \
#         response_decorator_list_or_get_after_execution_onoff_pagination, \
#         response_modify_decorator_get_single_after_execution
from users.knox_views.views import LoginView as KnoxLoginView, LogoutAllView
from users.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.exceptions import APIException
from datetime import datetime


class CreateUserView(generics.CreateAPIView):
    """Create a new user in system"""
    permission_classes = [AllowAny]
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    # @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    # @response_modify_decorator_post
    def post(self, request, format=None):
        data = {}
        with transaction.atomic():
            user_exist = self.queryset.filter(
                email=request.data['email']).exists()
            if not user_exist:
                raise APIException(
                    None,
                    'You Have Entered An Invalid Email Address',
                    status_code=status.HTTP_400_BAD_REQUEST)
            user_is_active = self.queryset.filter(
                email=request.data['email'],
                is_active=True)
            if not user_is_active:
                # raise APIException(
                #     None, 'sorry, Account is not active !',
                #     status_code=status.HTTP_400_BAD_REQUEST)

                raise APIException(
                    {"Message":"sorry, Account is not active !",
                    "status_code":status.HTTP_400_BAD_REQUEST}
                )
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            response = super(LoginView, self).post(request, format=None)
            user_detials = self.queryset.get(email=user)
            user_detials.last_login = datetime.now()
            user_detials.save()
            profile_query = Profile.objects.filter(user=user)
            # if profile_query:
            #     theme = profile_query.get().current_theme.theme_name
            #     first_name = profile_query.get().firstname
            #     is_first_login = profile_query.get().is_firstLogin
            #     if not is_first_login:
            #         profile_query.update(is_firstLogin=True)
            #     data['is_first_login'] = is_first_login
            #     data['message'] = f'Hello {first_name}, Welcome Back!'
            # else:
            #     theme = 'Default'
            data['token'] = response.data['token']
            data['token_expiry'] = response.data['expiry']
            # data['theme'] = theme
            data['user_details'] = {
                        "user_id": user_detials.id,
                        "name": user_detials.name,
                        "email": user_detials.email,
            }
            user_is_super = user_is_active.filter(is_superuser=True)
            # try:
            #     if not user_is_super:
            #         tenant_user = user
            #         tenant_query_owner = Tenant.objects.filter(
            #             org_admin=tenant_user
            #         )
            #         tenant_query_user = TenantUserMapping.objects.filter(
            #             user=tenant_user
            #         )
            #         if tenant_query_owner:
            #             tenant = tenant_query_owner.get()
            #         elif tenant_query_user:
            #             tenant = tenant_query_user.get().tenant
            #         action = F'{user_detials.name} Login'
            #         auditlog = AuditLog(request, tenant, tenant_user)
            #         auditlog._create_log(action)

            # except Exception:
            #     pass

            return Response(data)


