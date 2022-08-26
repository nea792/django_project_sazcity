from asyncio.windows_events import NULL
from statistics import mode
from urllib import request
from wsgiref.simple_server import demo_app
from django.db import models
from accounts.models import Custom_user
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist

class Category(models.Model):
    category_name = models.CharField(max_length = 15)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "دسته های کلی"



class Category_item(models.Model):
    total_category = models.ForeignKey(Category, on_delete = models.CASCADE)
    inner_category_name = models.CharField(max_length = 15)

    def __str__(self):
        return self.inner_category_name

    class Meta:
        verbose_name_plural = "زیر دسته ها"


class Product(models.Model):
    category_item = models.ForeignKey(Category_item, on_delete = models.CASCADE)
    product_name = models.CharField(max_length = 15)
    product_description = models.TextField()
    price = models.DecimalField(max_digits = 9, decimal_places = 0)
    pic = models.ImageField(upload_to = 'product_pics')
    sold = models.IntegerField(default = 0) 
    
    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = "محصولات"

    def total_number(self):
        color_values = self.color_value_set.all()
        sum = 0 
        for color_value in color_values:
            sum += color_value.quantity
        return sum

    def existance(self):  
        result = ""
        if self.total_number() == 0:
            result = "موجود نیست"
        return result

    def get_discount(self):#calculate price with discount
       final_price = self.price * (100 - self.discount.percent)/100
       return final_price

    def avg_rate(self):
        try:
            comments = self.comment_set.filter(parent = None)
            sum_rates = 0
            length_of_comments = len(comments)
            for comment in comments:
                sum_rates += comment.rate
            avg_rates = round(sum_rates/length_of_comments, 1)
            return avg_rates       
        except:
            return 0


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(Custom_user, on_delete = models.CASCADE)
    content = models.TextField()
    rate = models.PositiveSmallIntegerField(default = 0, validators = [MaxValueValidator(5), MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add = True)
    unknown_user = models.BooleanField(default = False)
    active = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id} from {self.user}'
    class Meta:
        verbose_name_plural = "نظرات"


class Discount(models.Model):
    percent = models.DecimalField(max_digits = 4, decimal_places = 0)
    product = models.OneToOneField(Product, on_delete = models.CASCADE)

    def __str__(self):
        return f'discount :{self.percent}% for {self.product}'

    class Meta:
        verbose_name_plural = "تخفیف ها"


class Attributes(models.Model):
    att_name = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.att_name}'

    class Meta:
        verbose_name_plural = "مشخصات"


class Attributes_value(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    att = models.ForeignKey(Attributes, on_delete = models.CASCADE)
    value = models.CharField(max_length = 25)

    def __str__(self):
        return f'{self.att} for {self.product}'

    class Meta:
        verbose_name_plural = "مقدار مشخصات"

        
class Liked_product(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(Custom_user, on_delete = models.CASCADE)
    added_date =  models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.user} for {self.product}'

    class Meta:
        verbose_name_plural = "لایک شده ها"

    
class Color(models.Model):
    color_name = models.CharField(max_length = 25)

    def __str__(self):
        return self.color_name

    class Meta:
        verbose_name_plural = "رنگ ها"


class Color_value(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    color = models.ForeignKey(Color, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 0) 

    def __str__(self):
        return f'{self.color} for {self.product}'

    class Meta:
        verbose_name_plural = "مقدار رنگ ها"


class Delivery(models.Model):
    type = models.CharField(max_length=25)
    price = models.DecimalField(max_digits = 9, decimal_places = 0)
    days = models.CharField(max_length=4, default='2')

    def __str__(self):
        return f'{self.type}'
    
    def get_total_days(self):
        return f'سفارش شما تا {self.days} روز کاری ارسال خواهد شد'

    class Meta:
        verbose_name_plural = "نحوه های ارسال"


class Order(models.Model):
    user = models.ForeignKey(Custom_user, on_delete=models.CASCADE, null=True, blank=True)
    delivery = models.ForeignKey(Delivery ,on_delete=models.CASCADE, null=True)
    complete = models.BooleanField (default = False)
    date_ordered =  models.DateTimeField(auto_now = True)
    confirm = models.BooleanField (default = False)
    
    class Meta:
        verbose_name_plural = "سبد های خرید"

    def __str__(self):
        return f'id : {self.id}'
    
    def update_quantity(self):
        if self.complete==True:
            items= self.order_items_set.all()
            for item in items:
                product =  item.product
                product.sold += item.qunatity
                product.save()
                
                color_value = Color_value.objects.filter(product=product, color=item.color)[0]
                color_value.quantity -= item.qunatity
                color_value.save()
    
    def total_product_price(self): #without delivery cost
        return sum([item.get_total_price() for item in self.order_items_set.all()])

    def total_price(self): #price with delivery cost
        product_price = self.total_product_price()
        return product_price + self.get_delivery_price()

    def get_delivery_price(self):
        if self.is_free_delivery():
            return 0
        else:
            return self.delivery.price * self.get_total_weight()

    def is_free_delivery(self):
        user_rate = self.user.rate
        if user_rate > 500 :
            return True
        return False
    
    def calculate_userRate(self):
        if self.complete==True:
            self.decrease_userRate()
            self.increase_userRate()
        
    def decrease_userRate(self):
        if self.is_free_delivery():
           self.user.rate -=500
           self.user.save()

    def increase_userRate(self):
        price =self.total_product_price()
        rate = round(price/200000)
        #print(price,rate)
        self.user.rate += rate
        self.user.save()

    def get_total_weight(self):
        return sum([item.get_weight() for item in self.order_items_set.all()])

    def get_total_quantity(self):
        return sum([item.qunatity for item in self.order_items_set.all()])

    def state(self):
        if self.complete==False:
            return 'ثبت نشده'
        else:
            return 'ثبت شده'
    

class Order_items(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, blank=True, null=True)
    added_date =  models.DateTimeField(auto_now_add = True)
    qunatity = models.IntegerField(default = 1)
    color = models.ForeignKey(Color, on_delete = models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "آیتم های سبد خرید"

    def __str__(self):
        return f'id : {self.id}'

    def get_total_price(self):
        if hasattr(self.product,'discount'):
             return self.qunatity * self.product.get_discount()
        else:
             return self.qunatity * self.product.price

    def get_weight(self):
        try:
             value_weight = self.product.attributes_value_set.get(att__att_name = 'وزن').value
             item_weight = float(value_weight)
        except:
            item_weight = 5

        return self.qunatity * round(item_weight)



