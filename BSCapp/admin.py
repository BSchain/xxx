from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Data)
admin.site.register(Transaction)
admin.site.register(Coin)
# admin.site.register(Recharge)
admin.site.register(Wallet)
admin.site.register(Purchase)
admin.site.register(Admin)
admin.site.register(Review)
admin.site.register(Notice)
admin.site.register(Block)
