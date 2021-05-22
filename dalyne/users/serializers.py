from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from core_module.models import Profile, UserPlans, Tenant
from rest_framework import serializers
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from custom_exception_message import CustomAPIException
from datetime import datetime
from rest_framework.exceptions import APIException
from django.contrib.sites.shortcuts import get_current_site
from users.tasks import send_mail_for_account_activation
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from core_module.utils import generate_token


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    company_name = serializers.CharField(required=False)
    plans = serializers.IntegerField(required=False)
    email = serializers.CharField(required=False)
    phone_no = serializers.CharField(required=False)
    firstname = serializers.CharField(required=False)
    lastname = serializers.CharField(required=False)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=False
    )
    user = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = (
            'company_name', 'plans', 'email', 'phone_no',
            'firstname', 'password', 'user', 'lastname',
        )

    def _exist_or_not_validator(self, exists_or_not):
        if exists_or_not:
            raise CustomAPIException(
                None,
                "email already exists",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        else:
            return True

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        with transaction.atomic():
            request = self.context.get('request')
            company_name = validated_data.get('company_name')
            plans = validated_data.pop('plans')
            firstname = validated_data.get('firstname')
            lastname = validated_data.get('lastname')
            email = validated_data.get('email')
            phone_no = validated_data.get('phone_no')
            password = validated_data.get('password')
            exists_or_not = get_user_model().objects.filter(
                email=email
            ).exists()
            self._exist_or_not_validator(exists_or_not)
            try:
                user = get_user_model().objects. \
                    create_user(
                    email=email,
                    name=firstname + " " + lastname,
                    password=password
                )
                user.is_active = True
                user.save()
                profile = Profile.objects.create(
                    user=user,
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    phone_no=phone_no
                )
                tenant, created = Tenant.objects.get_or_create(
                    org_admin=user,
                    company_name=company_name,
                )

                UserPlans.objects.create(
                    user=user,
                    tenant=tenant,
                    plans_id=plans
                )

            except Exception as e:
                raise e
                # raise CustomAPIException(
                #     None,
                #     "error ! bad request please check input",
                #     status_code=status.HTTP_400_BAD_REQUEST
                # )

            validated_data['user'] = user
            validated_data.pop('password')
            return validated_data


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            msg = _('Invalid Login Credentials. Please Check Your Username & Password')
            raise CustomAPIException(
                None, msg,
                status_code=status.HTTP_400_BAD_REQUEST)
        attrs['user'] = user
        return attrs
