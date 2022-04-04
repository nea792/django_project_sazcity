from django.contrib import admin
from .models import Category, Product, Discount, Attributes, Attributes_value, Comment, Liked_product
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(Attributes)
admin.site.register(Attributes_value)
admin.site.register(Comment)
admin.site.register(Liked_product)

