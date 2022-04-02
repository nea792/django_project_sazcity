from django.contrib import admin
from .models import Category, Product, Discount, Attributes, Attributes_value, Comment
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(Attributes)
admin.site.register(Attributes_value)
admin.site.register(Comment)

