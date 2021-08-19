from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from core_module.models import Profile, UserPlans, Tenant, UserOtp
from rest_framework import serializers, exceptions
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


class UserOtpSerializer(serializers.Serializer):
    email = serializers.CharField(required=True,
                                  allow_null=False,
                                  allow_blank=False
                                  )

    class Meta:
        fields = ('email',)


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=255)
    email = serializers.CharField()

    def validate(self, data):
        otp = data['otp']
        try:
            self.user_otp = UserOtp.objects.get(otp=otp, email=data['email'])
        except UserOtp.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")
        return data


class ProfileSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    total_download_points = serializers.SerializerMethodField()
    total_search_points = serializers.SerializerMethodField()
    remaining_download_points = serializers.SerializerMethodField()
    remaining_search_points = serializers.SerializerMethodField()

    def get_total_search_points(self, obj):
        try:
            return obj.user.userplans_set.first().plans.searches
        except:
            return None

    def get_total_download_points(self, obj):
        try:
            return obj.user.userplans_set.first().plans.download_points
        except:
            return None

    def get_remaining_download_points(self, obj):
        try:
            return obj.user.tenant.user_downloads.first().remaining_points
        except:
            return None

    def get_remaining_search_points(self, obj):
        return None

    def get_company_name(self, obj):
        try:
            return obj.user.tenant.company_name
        except:
            return None

    class Meta:
        model = Profile
        fields = ('firstname', 'lastname', 'email', 'phone_no', 'profile_pic', 'company_name',
                  'total_download_points', 'total_search_points', 'remaining_search_points',
                  'remaining_download_points')


class ChangePasswordSerializer(serializers.Serializer):
    """ change password serializer """
    new_password = serializers.CharField(style={'input_type': 'password'},
                                         trim_whitespace=False,
                                         required=True
                                         )
    old_password = serializers.CharField(write_only=True)

    def validate_old_password(self, attrs):
        if self.context['request'].user.check_password(attrs):
            return attrs
        else:
            raise serializers.ValidationError("Please enter correct password")

    def validate_new_password(self, data):

        if self.context['request'].user.check_password(data):
            raise exceptions.ValidationError("New password cannot be same as old password")
        if len(data) == 0:
            raise exceptions.ValidationError("New password should not be empty")
        return data
