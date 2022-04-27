from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
import jwt


class Currency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.symbol}"


class User(AbstractUser):
    otp = models.IntegerField(default=0, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    main_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, db_constraint=False)

    is_noob = models.BooleanField(default=True)
    is_elite = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_noob:
            user_role = "Noob"
        elif self.is_elite:
            user_role = "Elite"
        elif self.is_admin:
            user_role = "Admin"
        else:
            user_role = None

        return f"{self.first_name} {self.last_name} (Role={user_role})"

    @property
    def token(self):
        tk = jwt.encode({'user': self.username, 'email': self.email, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, algorithm='HS512')
        return tk


class Wallet(models.Model):
    name = models.CharField(max_length=100)
    username_id = models.ForeignKey(User, on_delete=models.CASCADE)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.currency_id.name} WALLET for {self.username_id.first_name} {self.username_id.last_name} | Amount = {self.amount} {self.currency_id.symbol}"
