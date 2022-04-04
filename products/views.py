from django.shortcuts import redirect, render
from .models import Category, Product, Liked_product
from .forms import Comment_Form


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
    product = Product.objects.get(id = pk)
    comment_form = Comment_Form()
    comments = product.comment_set.all()

    context={
        'product' : product ,
        'comments' : comments,
        'create_comment' : comment_form
    }
    
    return render(request, 'products/detail_product.html', context)


def send_comment(request, pk):
    
    if request.method == "POST":
        comment_form = Comment_Form(request.POST)

        if comment_form.is_valid():
            instance = comment_form.save(commit = False)
            instance.user = request.user
            instance.product = Product.objects.get(id = pk)
            instance.rate = request.POST['rate']
            instance.save()

            return redirect('products:detail-product', pk)


def add_likes(request, pk):

    if request.method == "POST":
        product = Product.objects.get(id = pk)
        user = request.user
        liked_by_user =user.liked_product_set.values('product')
    
        if not liked_by_user.filter(product = product):
            instance = Liked_product(product = product, user = user)
            instance.save()

        return redirect('products:detail-product', pk)
        
