from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    """Custom manager for the Account model."""

    def create_user(self, email, full_name, phone, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, phone, password=None):
        """Create and return a superuser."""
        user = self.create_user(email, full_name, phone, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """Account model to store user account details."""

    # Fields for account details
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    account_type = models.CharField(
        max_length=50,
        choices=[('savings', 'Savings'), ('checking', 'Checking'), ('business', 'Business')],
        default='savings'
    )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Authentication and permissions
    password = models.CharField(max_length=255)  
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 

    # Metadata
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    objects = AccountManager()

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        """Check if the user has the given permission."""
        return self.is_admin

    def has_module_perms(self, app_label):
        """Check if the user has permission to view the app."""
        return True


class Transaction(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} for {self.account.email}"
