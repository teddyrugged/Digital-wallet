from django.contrib import admin
from .models import (User, Currency, BaseQuoteSymbol, WalletType, Wallet, Rate)


admin.site.register(User)
admin.site.register(Currency)
admin.site.register(BaseQuoteSymbol)
admin.site.register(WalletType)
admin.site.register(Wallet)
admin.site.register(Rate)
