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


class Tenant(models.Model):
    org_admin = models.OneToOneField(
            User, on_delete=models.CASCADE, blank=True, null=True)
    company_name = models.CharField(
            max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='Tenant_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(
            User, related_name='Tenant_owned_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='Tenant_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("Tenant")


class Profile(models.Model):
    user = models.OneToOneField(
            User, on_delete=models.CASCADE, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_no = models.CharField(max_length=255, blank=True, null=True)
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


class Plans(models.Model):

    DATE_POSTFIX = (
        ('days', 'days'),
        ('months', 'months'),
        ('year', 'year'),
        ('quaterly', 'quaterly'),

    )
    CHOICES = (
        ('Per Qtr', 'Per Qtr'),
        ('Per year', 'Per year'),
    )

    name = models.CharField(
            max_length=255, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    pakage_validity = models.IntegerField(blank=True, null=True)
    pakage_postfix = models.CharField(
        max_length=50,
        choices=DATE_POSTFIX,
        default='months'
        )
    download_points = models.IntegerField(blank=True, null=True)
    unlimited_data_access = models.IntegerField(blank=True, null=True)
    unlimited_data_access_postfix = models.CharField(
        max_length=50,
        choices=DATE_POSTFIX,
        default='months'
        )
    workspaces = models.IntegerField(blank=True, null=True)
    searches = models.CharField(
            max_length=255, blank=True, null=True)
    workspaces_validity = models.IntegerField(blank=True, null=True)
    workspaces_validity_postfix = models.CharField(
        max_length=50,
        choices=DATE_POSTFIX,
        default='months'
        )
    workspaces_deletion_per_qtr = models.IntegerField(blank=True, null=True)
    shipment_limit_in_workspaces = models.IntegerField(blank=True, null=True)
    add_on_points_Facility = models.BooleanField(default=False)
    hot_products = models.IntegerField(blank=True, null=True)
    hot_products_postfix = models.CharField(
        max_length=50,
        choices=CHOICES,
        default='Per Qtr'
        )
    hot_company = models.IntegerField(blank=True, null=True)
    hot_company_postfix = models.CharField(
        max_length=50,
        choices=CHOICES,
        default='Per Qtr'
        )
    user = models.IntegerField(blank=True, null=True)
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
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,
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
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='Country_master_created_by',
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
        verbose_name_plural = _("CurrencyMaster")


class ImportTable(models.Model):
            
    BE_DATE = models.DateTimeField(blank=True, null=True)
    MONTH = models.CharField(
            max_length=10, blank=True, null=True)
    YEAR = models.IntegerField(blank=True, null=True)
    RITC = models.BigIntegerField(blank=True, null=True)
    TWO_DIGIT = models.IntegerField(blank=True, null=True)
    FOUR_DIGIT = models.IntegerField(blank=True, null=True)
    RITC_DISCRIPTION = models.TextField(blank=True, null=True)
    UQC = models.CharField(
            max_length=60, blank=True, null=True)
    QUANTITY = models.DecimalField(max_digits=15, decimal_places=2,
                 blank=True, null=True)
    CURRENCY = models.TextField(null=True, blank=True)
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
    EXPORTER_NAME = models.TextField(blank=True, null=True)
    EXPORTER_ADDRESS = models.TextField(blank=True, null=True)
    COUNTRY_OF_ORIGIN = models.TextField(blank=True, null=True)
    PORT_OF_LOADING = models.TextField(blank=True, null=True)
    PORT_OF_DISCHARGE = models.TextField(blank=True, null=True)
    PORT_CODE = models.CharField(max_length=60, blank=True, null=True)
    MODE_OF_PORT  = models.CharField(max_length=60, blank=True, null=True)
    IMPORTER_ID = models.TextField(blank=True, null=True)
    IMPORTER_NAME  = models.TextField(blank=True, null=True)
    IMPORTER_ADDRESS = models.TextField(blank=True, null=True)
    IMPORTER_CITY_STATE = models.TextField(blank=True, null=True)
    IMPORTER_PIN = models.CharField(max_length=60, blank=True, null=True)
    IMPORTER_PHONE = models.CharField(max_length=60, blank=True, null=True)
    IMPORTER_EMAIL = models.TextField(blank=True, null=True)
    IMPORTER_CONTACT_PERSON = models.TextField(blank=True, null=True)
    BE_TYPE = models.CharField(max_length=120, blank=True, null=True)
    CHA_NAME = models.TextField(blank=True, null=True)
    Item_No = models.IntegerField(blank=True, null=True)
    COUNTRY = models.ForeignKey(CountryMaster, related_name='ImportTable_COUNTRY',
                 on_delete=models.CASCADE, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='ImportTable_created_by',
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


class ExportTable(models.Model):    
    SB_DATE = models.DateTimeField(blank=True, null=True)
    MONTH = models.CharField(
            max_length=10, blank=True, null=True)
    YEAR = models.IntegerField(blank=True, null=True)
    RITC = models.BigIntegerField(blank=True, null=True)
    TWO_DIGIT = models.IntegerField(blank=True, null=True)
    FOUR_DIGIT = models.IntegerField(blank=True, null=True)
    RITC_DISCRIPTION = models.TextField(blank=True, null=True)
    UQC = models.CharField(
            max_length=60, blank=True, null=True)
    QUANTITY = models.DecimalField(max_digits=15, decimal_places=2,
                 blank=True, null=True)
    CURRENCY = models.TextField(null=True, blank=True)
    UNT_PRICE_FC = models.DecimalField(max_digits=20, decimal_places=7,
            blank=True, null=True)
    INV_VALUE_FC = models.DecimalField(max_digits=20, decimal_places=7,
            blank=True, null=True)
    UNT_PRICE_INR = models.DecimalField(max_digits=15, decimal_places=2,
            blank=True, null=True)
    INVOICE_NO = models.CharField(max_length=40, blank=True, null=True)
    SB_NO = models.BigIntegerField(blank=True, null=True)
    UNIT_RATE_WITH_FOB = models.DecimalField(max_digits=25, decimal_places=10,
            blank=True, null=True)
    PER_UNT_FOB = models.DecimalField(max_digits=25, decimal_places=10,
            blank=True, null=True)
    FOB_INR = models.DecimalField(max_digits=20, decimal_places=7,
            blank=True, null=True)
    FOB_FC = models.DecimalField(max_digits=25, decimal_places=10,
        blank=True, null=True)
    FOB_USD = models.DecimalField(max_digits=25, decimal_places=10,
        blank=True, null=True)
    EXCHANGE_RATE = models.IntegerField(blank=True, null=True)
    IMPORTER_NAME = models.TextField(blank=True, null=True)
    IMPORTER_ADDRESS = models.TextField(blank=True, null=True)
    COUNTRY_OF_ORIGIN = models.TextField(blank=True, null=True)
    PORT_OF_LOADING = models.TextField(blank=True, null=True)
    PORT_OF_DISCHARGE = models.TextField(blank=True, null=True)
    PORT_CODE = models.CharField(max_length=60, blank=True, null=True)
    MODE_OF_PORT  = models.CharField(max_length=60, blank=True, null=True)
    EXPORTER_ID = models.TextField(blank=True, null=True)
    EXPORTER_NAME = models.TextField(blank=True, null=True)
    EXPORTER_ADDRESS = models.TextField(blank=True, null=True)
    EXPORTER_CITY = models.TextField(blank=True, null=True)
    EXPORTER_STATE = models.TextField(blank=True, null=True)
    EXPORTER_PIN = models.CharField(max_length=60, blank=True, null=True)
    EXPORTER_PHONE = models.CharField(max_length=60, blank=True, null=True)
    EXPORTER_EMAIL = models.TextField(blank=True, null=True)
    EXPORTER_CONTACT_PERSON = models.TextField(blank=True, null=True)
    COUNTRY = models.ForeignKey(CountryMaster, related_name='ExportTable_COUNTRY',
                 on_delete=models.CASCADE, blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='ExportTable_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='ExportTable_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("ExportTable")


class ProductMaster(models.Model):
    hs_code = models.CharField(
            max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
            User, related_name='ProductMaster_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='ProductMaster_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("ProductMaster")


class CompanyMaster(models.Model):
    iec_code = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    location = models.CharField(
        max_length=60, null=True, blank=True
    )
    created_by = models.ForeignKey(
            User, related_name='CompanyMaster_created_by',
            on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(
            User, related_name='CompanyMaster_updated_by',
            on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = _("CompanyMaster")


class MailTemplate(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    html_content = models.TextField(blank=True, null=True)
    template_variable = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _("Mail Template")

    def __str__(self):
        return self.name
