from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from core_module.models import Profile, Company, UserPlans
from rest_framework import serializers
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# from core.utils import generate_token
from datetime import datetime

from rest_framework.exceptions import APIException

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

    def _pass_validation(self, password):
        if len(password) < 8:
            # raise APIException(
            #     None,
            #     "password must be equal or greater than 8 char",
            #     status_code=status.HTTP_400_BAD_REQUEST
            #     )
            raise APIException(
                {"Message":"password must be equal or greater than 8 char",
                "status_code":status.HTTP_400_BAD_REQUEST}
            )
        else:
            return True

    def _exist_or_not_validator(self, exists_or_not):
        if exists_or_not:
            # raise APIException(
            #     None,
            #     "email already exists",
            #     status_code=status.HTTP_400_BAD_REQUEST
            #     )
            raise APIException(
                    {"Message":"email already exists",
                    "status_code":status.HTTP_400_BAD_REQUEST}
                )
        else:
            return True

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        with transaction.atomic():
            request = self.context.get('request')
            company_name = validated_data.pop('company_name')
            plans = validated_data.pop('plans')
            firstname = validated_data.get('firstname')
            lastname = validated_data.get('lastname')
            email = validated_data.get('email')
            phone_no = validated_data.get('phone_no')
            password = validated_data.get('password')
            # self._pass_validation(password)
            # rua_check = 'mailto:dmarc.reports@rua.secureyourinbox.net'
            # ruf_check = 'mailto:forensic.reports@ruf.secureyourinbox.net'
            exists_or_not = get_user_model().objects.filter(
                                    email=validated_data.get(
                                        'email'
                                        )
                                    ).exists()
            self._exist_or_not_validator(exists_or_not)
            try:
                user = get_user_model().objects.\
                                create_user(
                                    email=validated_data.get('email'),
                                    name=firstname+" "+lastname,
                                    password=password
                                )
                user.is_active = True
                user.save()
                profile = Profile.objects.create(
                        user=user,
                        firstname=firstname,
                        lastname=lastname,
                        email=validated_data.get('email'),
                        phone_no=phone_no
                    )
                company_id, created = Company.objects.get_or_create(
                        name=company_name.strip())
                UserPlans.objects.create(
                        user=user,
                        company=company_id,
                        plans_id=plans
                    )                

            except Exception:
                raise APIException(
                    {"Message":"error ! bad request please check input",
                    "status_code":status.HTTP_400_BAD_REQUEST}
                )
            
            validated_data['company_name'] = company_name
            validated_data['user'] = user
            # domain = self._url_handler(current_site)
            # uid = urlsafe_base64_encode(force_bytes(user.pk))
            # token = generate_token.make_token(user)
            # ip = get_client_ip(request)
            # name = firstname + " " + lastname
            # send_mail_for_account_activation.delay(
            #     email,
            #     name,
            #     domain,
            #     uid,
            #     token,
            #     ip
            # )
            # default_theme_exists = Theme.objects.filter(
            #     theme_name='Default')
            # if default_theme_exists:
            #     Profile.objects.filter(
            #         id=str(profile)).update(
            #             current_theme=default_theme_exists.get().id)
            # else:
            #     theme = Theme.objects.create(
            #         theme_name='Default')
            #     Profile.objects.filter(
            #         id=profile).update(
            #             current_theme=theme)

            # ip = get_client_ip(request)
            # geo_data = get_ip_location(ip)
            # AuditTable.objects.create(
            #     tenant=tenant,
            #     username=user,
            #     timestamp=datetime.now(),
            #     ip_address=ip,
            #     continent_code=geo_data[
            #                 'continent_code'
            #                 ] if 'continent_code' in geo_data else None,
            #     continent_name=geo_data['continent_name'],
            #     country_code=geo_data['country_code'],
            #     country_name=geo_data['country_name'],
            #     region_code=geo_data['region_code'],
            #     region_name=geo_data['region_name'],
            #     city=geo_data['city'],
            #     country_flag=geo_data['location']['country_flag'],
            #     country_flag_emoji=geo_data[
            #         'location']['country_flag_emoji'],
            #     action=email + ' Signup'
            # )
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
            # raise APIException(
            #         None, msg,
            #         status_code=status.HTTP_400_BAD_REQUEST)
            raise APIException(
                    {"Message":"Invalid Login Credentials. Please Check Your Username & Password",
                    "status_code":status.HTTP_400_BAD_REQUEST}
                )
        attrs['user'] = user
        return attrs