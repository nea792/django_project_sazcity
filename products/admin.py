from django.contrib import admin
from .models import *

 #Category                
admin.site.register(Category)

#Category_item
class Category_itemAdmin(admin.ModelAdmin):
    list_display = ['inner_category_name', 'get_category']
    search_fields = ['inner_category_name', 'total_category__category_name']
    list_filter = ['total_category']

    @admin.display(description='category')
    def get_category(self, instance):
        return instance.total_category.category_name

admin.site.register(Category_item, Category_itemAdmin)

#product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'get_category', 'price', 'sold']
    search_fields = ['product_name', 'category_item__inner_category_name']
    list_filter = ['category_item']

    @admin.display(description='category', ordering='category_item__inner_category_name')
    def get_category(self, instance):
        return instance.category_item.inner_category_name

admin.site.register(Product, ProductAdmin)

#discount
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['percent', 'product']
 
admin.site.register(Discount, DiscountAdmin)

#attributes
class AttributesAdmin(admin.ModelAdmin):
    list_display = ['att_name']
    search_fields = ['att_name']

admin.site.register(Attributes, AttributesAdmin)

#attributes_value
class Attributes_valueAdmin(admin.ModelAdmin):
    list_display = ['product', 'att', 'value']
    list_filter = ['product']
    
admin.site.register(Attributes_value, Attributes_valueAdmin)

#comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'product', 'rate', 'active', 'unknown_user', 'parent']
    list_filter = ['active', 'date']
    actions = ['approve_comments' , 'reply']

    def reply(self, request, queryset):
        for obj in queryset:
            reply = Comment(user = request.user, parent = obj , product =obj.product, content="تشکر از شما" )
            reply.save()

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    
admin.site.register(Comment, CommentAdmin)

#liked product
class Liked_productAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
    list_filter = ['added_date']
    
admin.site.register(Liked_product, Liked_productAdmin)

#color value
class Color_valueAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'quantity']
    search_fields = ['product__product_name', 'color__color_name']
    list_filter = ['product']

admin.site.register(Color_value, Color_valueAdmin)

#color
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color_name']
    search_fields = ['color_name']

admin.site.register(Color, ColorAdmin)

#order
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'complete', 'get_quantity', 'get_price', 'get_deliveryType', 'confirm']
    search_fields = ['user__username']
    list_filter = ['complete','date_ordered' , 'confirm']
    actions = ['confirm_order']

    def confirm_order(self, request, queryset):
        queryset.update(confirm=True)
    
    @admin.display(description='Qunatity')
    def get_quantity(self, instance):
        try:
           return instance.get_total_quantity()
        except:
            return '0'
          
    @admin.display(description='Price')
    def get_price(self, instance):
        try:
            return instance.total_price()
        except:
            return '0'
    
    @admin.display(description='Delivery')
    def get_deliveryType(self, instance):
        try:
            return instance.delivery.type
        except:
            return 'none'
    
admin.site.register(Order, OrderAdmin)

#order_itema
class Order_itemsAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'get_order', 'product', 'qunatity', 'color']
    search_fields = ['order__user__username', 'order__id']
 
    @admin.display(description='user', ordering='order__user__username')
    def get_user(self, instance):
        try:
            return instance.order.user
        except:
            return 'unknown'

    @admin.display(description='order code', ordering='order__id')
    def get_order(self, instance):
        return instance.order.id
    
admin.site.register(Order_items, Order_itemsAdmin)

#delivery
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['type', 'price']
    
admin.site.register(Delivery,DeliveryAdmin)




'''
class ReplyAdmin(admin.ModelAdmin):
    fields = ['parent','content']
    list_display = ['user', 'parent']
    list_filter =['date']

    def formfield_for_foreignkey(self, instance, request, **kwargs):
        if instance.name == "parent":
            kwargs["queryset"] = Comment.objects.filter(name__in=['God', 'Demi God'])
        return super().formfield_for_foreignkey(instance, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Reply , ReplyAdmin)

'''