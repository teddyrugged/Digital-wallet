from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=200)
    is_noob = models.BooleanField(default=False)
    is_elite = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username

class Currency(models.Model):
    # (United Arab Emirates Dirham/British Pound, British Pound/Japanese Yen)
    name = models.CharField(max_length=100) 
    # (AED/GBP,JPY/EUR,CAD/AUD,CHF/CNY,USD/JPY)
    symbol = models.CharField(max_length=10) 
    
    def __str__(self):
        return self.symbol

class BaseQuoteSymbol(models.Model):
    # (British Pound/Japanese Yen)
    name = models.CharField(max_length=100)
    # (GBP/JPY) 
    pair = models.CharField(max_length=100) 

    def __str__(self):
        return self.pair   

class WalletType(models.Model):
    # (AED_WALLET/USD_WALLET/UNIVERSAL)
    name = models.CharField(max_length=100)
    # (Currency.id) 
    currency_id = models.ManyToManyField(Currency) 
    
    def __str__(self):
        return self.name      

class Wallet(models.Model):
    # (User.id)
    username_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # (WalletType.id) 
    wallet_type_id = models.ForeignKey(WalletType, on_delete=models.CASCADE) 
    # (20.72555)
    amount = models.FloatField() 
    
    def __str__(self):
        return self.wallet_type_id.name

class Rate(models.Model):
    # (Currency.id)
    base_currency_id = models.ForeignKey(Currency, related_name="base_currency_id", on_delete=models.CASCADE)
    # (Currency.id) 
    quote_currency_id = models.ForeignKey(Currency, related_name="quote_currency_id", on_delete=models.CASCADE) 
    # (BaseQuoteSymbol.id)
    base_quote_symbol_id = models.ForeignKey(BaseQuoteSymbol, on_delete=models.CASCADE)
    # (0.92708) 
    current_rate = models.FloatField()
    
    def __str__(self):
        return self.base_quote_symbol_id.pair
