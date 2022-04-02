from django.db import models
from accounts.models import Custom_user
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    category_name = models.CharField(max_length = 15)
    category_description = models.TextField()
    pic = models.ImageField(upload_to = 'category_pics')

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    product_name = models.CharField(max_length = 15)
    product_description = models.TextField()
    price = models.DecimalField(max_digits = 9, decimal_places = 0)
    pic = models.ImageField(upload_to = 'product_pics')
    total_number = models.IntegerField() 
    liked = models.ManyToManyField(Custom_user, blank=True )
   
    def __str__(self):
        return self.product_name

    def existance(self):  
        result = ""
        if self.total_number == 0:
            result = "موجود نیست"
        return result

    def get_discount(self):
       final_price = self.price * (100 - self.discount.percent)/100
       return final_price


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(Custom_user, on_delete = models.CASCADE)
    title = models.CharField(max_length = 25)
    content = models.TextField()
    rate = models.PositiveSmallIntegerField(default = 0, validators = [MaxValueValidator(5), MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add = True)
    unknown_user = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.title} from {self.user}'
    

class Discount(models.Model):
    percent = models.DecimalField(max_digits = 4, decimal_places = 0)
    product = models.OneToOneField(Product, on_delete = models.CASCADE)

    def __str__(self):
        return f'discount :{self.percent}% for {self.product}'


class Attributes(models.Model):
    att_name = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.att_name}'


class Attributes_value(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    att = models.ForeignKey(Attributes, on_delete = models.CASCADE)
    value = models.CharField(max_length = 25)

    def __str__(self):
        return f'{self.att} for {self.product}'
        





