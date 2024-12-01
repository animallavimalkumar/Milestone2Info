from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from .managers import UserManager
from django.utils import timezone


# User model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    groups = models.ManyToManyField(
        Group, related_name="finance_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="finance_user_permissions", blank=True
    )

    def _str_(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


# Category model
class Category(models.Model):
    INCOME = 'Income'
    EXPENSE = 'Expense'
    SAVINGS= 'Savings'
    INVESTMENT= 'Investment'
    DEBT= 'Debt'
    CATEGORY_TYPES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
        (SAVINGS, 'Savings'),
        (INVESTMENT, 'Investment'),
        (DEBT, 'Debt'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', blank=True, null=True)
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.name} ({self.category_type})"


# Income model
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'category_type': 'Income'}, related_name='income')
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.email} - {self.category.name} - {self.amount}"


# Expense model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'category_type': 'Expense'}, related_name='expenses')
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    is_fixed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.email} - {self.category.name} - {self.amount}"


# EMI model
class EMI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emis')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    frequency = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    next_payment_date = models.DateField()

    def _str_(self):
        return f"{self.user.email} - EMI {self.amount} - {self.frequency}"


# Budget model
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def _str_(self):
        return f"{self.user.email} - {self.category.name} Budget {self.amount_limit}"


# Alert model
class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    message = models.TextField(default='Default message')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"Alert for {self.user.email}: {self.message[:30]}"


# Report model
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    file_path = models.FileField(upload_to='reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Report for {self.user.email} - {self.report_type}"