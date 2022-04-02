from unicodedata import category
from django.shortcuts import render
from .models import Category, Product
from .forms import Create_comment


def show_category(request): 
    categories = Category.objects.all()
    context = {
        'categories' : categories ,
    }
    
    return render (request, 'products/category.html', context)


def show_products(request, name):
    id_category = Category.objects.get(category_name = name).id

    if 'filter' in request.GET:
        products = Product.objects.filter(category = id_category).order_by('-id')
    else:
        products = Product.objects.filter(category = id_category)

    context = {
        'products' : products ,
    }
     
    return render (request, 'products/product.html', context)


def detail_product(request, pk):
    create_comment = Create_comment()
    product = Product.objects.get(id = pk)
    comments = product.comment_set.all()

    context={
        'product' : product ,
        'comments' : comments,
        'create_comment' : create_comment
    }
    
    return render(request, 'products/detail_product.html', context)