from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL
CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
STATUS = (
	('Pending', 'Pending'), 
	('Completed', 'Completed')
)

WITHDRAW_CHOICE = (
	('Bank', 'Bank'), 
	('Bitcoin', 'Bitcoin')
)
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user




class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    mobile_no = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    wallet = models.OneToOneField('Wallets', on_delete=models.CASCADE, max_length=250, blank=True, null=True, related_name='wallet')
    amount = models.CharField(max_length=250, null=True, blank=True, default=0.0)
    payment_method = models.CharField(max_length=250, null=True, blank=True, choices=WITHDRAW_CHOICE, default='Bitcoin')
    slug = models.SlugField(max_length=250,blank=True, null=True)

    date_created = models.DateTimeField(max_length=250, null=True, blank=True, default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.email)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.user} profile'

class Wallets(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True, default='3L8rpKiJvzHWFPURbyfrexR9nzzaAwFPGQ')
    balance = models.CharField(max_length=250, null=True, blank=True, default=0.0)
    profit_margin = models.FloatField(max_length=250, null=True, blank=True, default=0.0)
    deposit = models.ForeignKey('Deposits', null=True, blank=True, on_delete=models.CASCADE)
    withdrawals = models.ForeignKey('Withdraw', null=True, blank=True, on_delete=models.CASCADE)
    transactions = models.ForeignKey('Transaction', null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250,null=True, blank=True)
    
    this_week = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    this_month = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    this_week_roi = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    this_month_roi = models.CharField(max_length=250, blank=True, null=True, default=0.0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.email} {self.address}')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})
	
    def __str__(self):
        return f'{self.user} wallet'

class Banks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,max_length=250, null=True, blank=True)
    bank_name = models.CharField(max_length=250, null=True, blank=True, default=0.0)
    bank_address = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True )
    IBAN_number = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=250,null=True, blank=True, )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.email} bank')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})

    def __str__(self):
	    return f'{self.user.email} banks'


class Deposits(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,max_length=250, null=True, blank=True, )
    amount = models.CharField(max_length=250, null=True, blank=True, default=0.0)
    quick_trade = models.CharField(max_length=250, null=True, blank=True)
    payment_method = models.CharField(max_length=250, null=True, blank=True, choices=WITHDRAW_CHOICE, default='Bitcoin')
    slug = models.SlugField(max_length=250,null=True, blank=True, )
    status = models.CharField(choices=STATUS, default="Pending", max_length=250, null=True, blank=True)
    date_created = models.DateTimeField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.email} ${self.amount} {self.status} {self.date_created}')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})

    def __str__(self):
	    return f'{self.user} deposited ${self.amount}'  

class Transaction(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,max_length=250, null=True, blank=True)
    wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE, null=True, blank=True)
    withdraw = models.ManyToManyField('Withdraw', related_name='withdraw')
    deposit = models.ManyToManyField('Deposits', related_name='deposit')
    date_created = models.DateTimeField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=250,blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.email} history')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})

    def get_add_to_transaction_url(self):
        return reverse("core:add-to-transaction", kwargs={
            'slug': self.slug
        })

    def __str__(self):
	    return f'{self.user.email} {self.date_created}'


class Withdraw(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,max_length=250, null=True, blank=True,)
    amount = models.CharField(max_length=250, null=True, blank=True)
    withdrawal_method = models.CharField(choices=WITHDRAW_CHOICE, default='Bitcoin', max_length=250, null=True, blank=True)
    status = models.CharField(choices=STATUS, default="Pending", max_length=250, null=True, blank=True)
    withdrawal_date = models.DateTimeField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=250,null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.email} {self.amount} {self.status}')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})

    def __str__(self):
	    return f'{self.user.email} withdrawals'


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Wallets.objects.create(user=instance) 
        Transaction.objects.create(user=instance)
        print('[SIGNALS] Created Profile, Wallet and Transaction models')

def save_user_profile(sender, instance, **kwargs):
    instance.wallet.save()
    print('[SIGNALS] Add wallet to profile')

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

#post_save.connect(save_user_profile, sender=UserProfile)
#post_save.connect(save_transaction, sender=Transaction)