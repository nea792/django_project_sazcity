from pyexpat import model
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=15)
    category_description = models.TextField()
    pic= models.ImageField(upload_to='category_pics')

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=15)
    product_description = models.TextField()
    price= models.DecimalField(max_digits=9, decimal_places=0)
    pic = models.ImageField(upload_to='product_pics')
    total_number = models.IntegerField() 
    #spesific att
   

    def __str__(self):
        return self.product_name

    def existance(self):  
        result=""
        if self.total_number==0:
            result="موجود نیست"
        return result


'''
class Comment(models.Model):
    pass
'''

class Discount(models.Model):
    percent = models.DecimalField(max_digits=4, decimal_places=2)
    product = models.OneToOneField(Product, on_delete = models.CASCADE)

    def __str__(self):
        return f'discount :{self.percent}% for {self.product}'

''' # i dont have idea why i've created this model before
class Discount_item(models.Model):
    discount=models.ForeignKey(Discount, on_delete = models.CASCADE)
    product = models.OneToOneField(Product, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.discount} for {self.product}'



class Attributes(models.Model):
    att_name=models.CharField(max_length=25)

    def __str__(self):
        return f'{self.att_name}'
'''