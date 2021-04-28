from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """creates and save a new super User"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Profile(models.Model):
    user = models.OneToOneField(
            User, on_delete=models.CASCADE, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_no = models.BigIntegerField(blank=True, null=True)
    profile_pic = models.ImageField(
                    upload_to="avatar",
                    default="avatar/None/default.png"
                    )
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='profile_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(
            User, related_name='profile_owned_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='profile_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("profile")


class Company(models.Model):
    name = models.CharField(
            max_length=255, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='Company_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(
            User, related_name='Company_owned_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='Company_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("Company")


class Plans(models.Model):
    name = models.CharField(
            max_length=255, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    data_access_of_all_countries = models.TextField(
        blank=True, null=True)
    one_year_validity = models.CharField(
            max_length=255, blank=True, null=True)
    unlimited_full_shipment_view = models.CharField(
            max_length=255, blank=True, null=True)
    unlimited_importer_exporter_view = models.CharField(
            max_length=255, blank=True, null=True)
    unlimited_view_of_linkedin_contacts = models.CharField(
            max_length=255, blank=True, null=True)
    unlimited_view_charts_and_dashboard = models.CharField(
            max_length=255, blank=True, null=True)
    unlimited_searches = models.IntegerField(
            blank=True, null=True)
    number_of_workspaces = models.IntegerField(
            blank=True, null=True)
    workspace_deletion = models.IntegerField(
            blank=True, null=True)
    workspace_shipment_limit = models.BigIntegerField(
            blank=True, null=True)
    shipment_credits_for_excel_download = models.BigIntegerField(
            blank=True, null=True)
    roll_over_points_to_next_year = models.CharField(
            max_length=255, blank=True, null=True)
    download_buyers_or_suppliers_contact_profile = models.IntegerField(
            blank=True, null=True)
    contact_details_phone_and_email = models.IntegerField(
            blank=True, null=True)
    hot_products = models.IntegerField(
            blank=True, null=True)
    hot_companies = models.CharField(
            max_length=255, blank=True, null=True)
    users_count = models.IntegerField(
            blank=True, null=True)
    validity_of_days = models.IntegerField(
            blank=True, null=True) #Plan validity(days)

    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='Plans_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(
            User, related_name='Plans_owned_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='Plans_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("Plans")


class UserPlans(models.Model):
    user = models.ForeignKey(
            User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
            blank=True, null=True)
    plans = models.ForeignKey(
            Plans, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='UserPlans_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(
            User, related_name='UserPlans_owned_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='UserPlans_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("UserPlans")

class CountryMaster(models.Model):
    name = models.CharField(
            max_length=255, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='Country_master_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(
            User, related_name='Country_master_owned_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='Country_master_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("CountryMaster")

class CurrencyMaster(models.Model):
    name = models.CharField(
            max_length=255, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='Currency_master_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(
            User, related_name='Currency_master_owned_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='Currency_master_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("Currency")

class ImportTable(models.Model):
    name = models.CharField(
            max_length=255, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    data_access_of_all_countries = models.TextField(
        blank=True, null=True)
    workspace_shipment_limit = models.BigIntegerField(
            blank=True, null=True)
    
    BE_DATE = models.DateTimeField(blank=True, null=True)
    MONTH = models.CharField(
            max_length=10, blank=True, null=True)
    YEAR = models.IntegerField(blank=True, null=True)
    RITC = models.BigIntegerField(blank=True, null=True)
    TWO_DIGIT = models.IntegerField(blank=True, null=True)
    FOUR_DIGIT = models.IntegerField(blank=True, null=True)
    RITC_DISCRIPTION = models.TextField(blank=True, null=True)
    UQC = models.CharField(
            max_length=5, blank=True, null=True)
    QUANTITY = models.DecimalField(max_digits=15, decimal_places=2,
                 blank=True, null=True)
    CURRENCY = models.ForeignKey(CurrencyMaster, on_delete=models.CASCADE,
            blank=True, null=True)
    UNT_PRICE_FC = models.DecimalField(max_digits=20, decimal_places=7,
            blank=True, null=True)
    INV_VALUE_FC = models.DecimalField(max_digits=20, decimal_places=7,
            blank=True, null=True)
    UNT_PRICE_INR = models.DecimalField(max_digits=15, decimal_places=2,
            blank=True, null=True)
    INV_NO = models.IntegerField(blank=True, null=True)
    BE_NO = models.BigIntegerField(blank=True, null=True)
    UNT_RATE_WITH_DUTY = models.DecimalField(max_digits=25, decimal_places=10,
            blank=True, null=True)
    PER_UNT_DUTY = models.DecimalField(max_digits=25, decimal_places=10,
            blank=True, null=True)
    DUTY_INR = models.DecimalField(max_digits=20, decimal_places=7,
            blank=True, null=True)
    DUTY_FC = models.DecimalField(max_digits=25, decimal_places=10,
            blank=True, null=True)
    DUTY_PERCENT = models.DecimalField(max_digits=15, decimal_places=10,
            blank=True, null=True)
    EX_TOTAL_VALUE = models.DecimalField(max_digits=25, decimal_places=10,
            blank=True, null=True)
    ASS_VALUE_INR = models.DecimalField(max_digits=25, decimal_places=10,
            blank=True, null=True)
    ASS_VALUE_USD = models.DecimalField(max_digits=25, decimal_places=10,
            blank=True, null=True)
    ASS_VALUE_FC = models.DecimalField(max_digits=25, decimal_places=10,
            blank=True, null=True)
    EXCHANGE_RATE = models.IntegerField(blank=True, null=True)
    EXPORTER_NAME = models.CharField(
            max_length=30, blank=True, null=True)
    EXPORTER_ADDRESS = models.TextField(blank=True, null=True)
    COUNTRY_OF_ORIGIN = models.ForeignKey(CountryMaster, on_delete=models.CASCADE,
            blank=True, null=True)
    PORT_OF_LOADING = models.CharField(max_length=30, blank=True, null=True)
    PORT_OF_DISCHARGE = models.CharField(max_length=30, blank=True, null=True)
    PORT_CODE = models.CharField(max_length=10, blank=True, null=True)
    MODE_OF_PORT  = models.CharField(max_length=5, blank=True, null=True)
    IMPORTER_ID = models.CharField(max_length=15, blank=True, null=True)
    IMPORTER_NAME  = models.CharField(max_length=40, blank=True, null=True)
    IMPORTER_ADDRESS = models.TextField(blank=True, null=True)
    IMPORTER_CITY_STATE = models.CharField(max_length=20, blank=True, null=True)
    IMPORTER_PIN = models.CharField(max_length=10, blank=True, null=True)
    IMPORTER_PHONE = models.CharField(max_length=15, blank=True, null=True)
    IMPORTER_EMAIL = models.CharField(max_length=20, blank=True, null=True)
    IMPORTER_CONTACT_PERSON = models.CharField(max_length=30, blank=True, null=True)
    BE_TYPE = models.CharField(max_length=2, blank=True, null=True)
    CHA_NAME = models.CharField(max_length=30, blank=True, null=True)
    Item_No = models.IntegerField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='ImportTable_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(
            User, related_name='ImportTable_owned_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='ImportTable_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("ImportTable")

