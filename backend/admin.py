from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)    
admin.site.register(Order)
# admin.site.register(OrderDetail)
# admin.site.register(CartObject)
# admin.site.register(Location)