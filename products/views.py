from django.contrib import messages
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from accounts.forms import Profile_form
from django.shortcuts import get_object_or_404
from django.http import  Http404
from django.contrib.auth.decorators import permission_required


def show_products(request, name):#show products of each category
    id_category = get_object_or_404(Category_item,inner_category_name = name).id
    products = Product.objects.filter(category_item = id_category)
    filter = " "

    if 'filter' in request.GET:
        option_id = request.GET['filter']

        if option_id == '1' :
            products = products.order_by('-id')
            filter = "جدید"

        elif option_id == '2':
            products = sorted(products, key= lambda t: int(t.avg_rate()), reverse=True)
            filter = "محبوب"

        elif option_id == '3':
             products = products.order_by('-sold')
             filter = "پر فروش"

        else:
             raise Http404()
   

    context ={
        'products' :products,
        'filter' : filter
        }
    return render (request, 'products/product.html', context)


def result_search(request):
    try:
        query = request.GET.get("search")
        category_items = Category_item.objects.filter(inner_category_name__icontains=query)
        products = Product.objects.filter( product_name__icontains=query) |Product.objects.filter(category_item__in = category_items)
    except:
        raise Http404()

    context = {
        'products' : products ,
    }
     
    return render (request, 'products/product.html', context)


def detail_product(request, pk):
    product = get_object_or_404(Product, id = pk)
    comment_form = Comment_Form()
    comments = product.comment_set.filter(active=True , parent=None).order_by('-id')
    attributes = product.attributes_value_set.all()
    colors = product.color_value_set.filter( quantity__gt = 0)
    reply_form = Reply_Form()

    context={
        'product' : product ,
        'comments' : comments,
        'create_comment' : comment_form,
        'reply_form' : reply_form,
        'attributes' : attributes,
        'colors' : colors
    }
    
    return render(request, 'products/detail_product.html', context)


@login_required(login_url='/')  # return 302
def send_comment(request, pk):
    
    if request.method == "POST":
        comment_form = Comment_Form(request.POST)

        if comment_form.is_valid():
            instance = comment_form.save(commit = False)
            instance.user = request.user
            instance.product = Product.objects.get(id = pk)
            if 'rating' in request.POST:
               instance.rate = request.POST['rating']
            instance.save()

        return redirect('products:detail-product', pk)

    raise Http404()


@login_required(login_url='/')
#@permission_required("products.add_reply", raise_exception=True)# return 403
def send_reply(request,pk):
    if request.method == "POST":
        reply_from = Reply_Form(request.POST)
        parent_id = request.POST['parent_id']
        parent = Comment.objects.get(id = parent_id)
        product = parent.product

        if reply_from.is_valid():
            instance = reply_from.save(commit = False)
            instance.user = request.user
            instance.parent = parent
            instance.product = product
            instance.save()

        return redirect('products:detail-product', pk)

    raise Http404()


@login_required(login_url='/')  
def add_likes(request, pk):

    if request.method == "POST":
        product = Product.objects.get(id = pk)
        user = request.user
        #liked_by_user = user.liked_product_set.values('product')
        liked , created = Liked_product.objects.get_or_create(user=user, product=product)
    
        if created:
            messages.success(request, 'محصول مورد نظر به علاقه مندی ها اضافه شد')

        else:
            messages.warning(request, 'محصول مورد نظر را قبلا لایک کرده اید')

        return redirect('products:detail-product', pk)
    raise Http404()


@login_required(login_url='/')  
def add_order(request):
    if request.method=='POST':
        data = json.loads(request.body)
        productId = data['productId']
        colorValueId = data['colorValueId']
        product = Product.objects.get(id = productId)
        user = request.user
        color_value = Color_value.objects.filter(id=colorValueId, quantity__gt=0)
        
        order, created = Order.objects.get_or_create(user=user, complete=False)

        if product.total_number() > 0 and color_value:

            color = color_value[0].color
            order_item, created = Order_items.objects.get_or_create(order=order, product=product, color=color)
            if created:
                messages.success(request, 'محصول مورد نظر اضافه شد')
            if not created :
                messages.warning(request, 'محصول مورد نظر را قبلا اضافه کرده اید')
        else:
            messages.warning(request, 'محصول مورد نظر موجود نیست')

        return JsonResponse('add_order', safe=False)
    raise Http404()


@login_required(login_url='/')  
def update_order(request):
    if request.method=='POST':
        data = json.loads(request.body)
        orderItemId = data['orderItemId']
        action = data['action']
    
        order_item = Order_items.objects.get(id=orderItemId)
        color = order_item.color
        total_quantity = order_item.product.color_value_set.get(color=color).quantity

        if action=="add":
            remain_quantity = total_quantity - order_item.qunatity
            if remain_quantity > 0:
                order_item.qunatity = (order_item.qunatity + 1)
                order_item.save()

            else:
                messages.warning(request, 'محصول مورد نظر به این تعداد موجود نیست')

        elif action=="remove":
            order_item.qunatity -= 1
            order_item.save()

        if order_item.qunatity == 0 :
            messages.warning(request, 'محصول مورد نظر حذف شد')
            order_item.delete()

        return JsonResponse('update_order', safe=False)
    raise Http404()


@login_required(login_url='/')  
def show_likes(request):
    user = request.user
    likes = user.liked_product_set.all()

    context = {
        'likes' : likes
    }

    return render(request, 'products/userlikes.html', context)


@login_required(login_url='/')  
def show_cart(request):
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    order_items = order.order_items_set.all()
    deliveries = Delivery.objects.all()
    context ={
        'order_items': order_items,
        'order': order,
        'deliveries' : deliveries
    }
    return render(request, 'products/cart.html', context)


@login_required(login_url='/')  
def delete_liked(request, pk):
    if request.method=='POST':
        selected_item = Liked_product.objects.get(id = pk)
        messages.warning(request, 'محصول مورد نظر حذف شد')
        selected_item.delete()

        return redirect('products:liked-list')
    raise Http404()


@login_required(login_url='/')  
def delete_orderItem(request, pk):
    if request.method=='POST':
        selected_item = Order_items.objects.get(id = pk)
        messages.warning(request, 'محصول مورد نظر حذف شد')
        selected_item.delete()

        return redirect('products:show-cart')

    raise Http404()


def about_us(request):
    return render(request, 'products/about_us.html')


@login_required(login_url='/')  
def confirm_order(request):

    order = get_object_or_404(Order, user=request.user, complete=False)

    if Order_items.objects.filter(order=order).count()>0 and order.delivery:

        if request.method == "POST":
            profile_form = Profile_form(request.POST, instance=request.user.user_info)
        
            if profile_form.is_valid():
                profile_form.save()
                order.complete = True
                order.save()
                order.update_quantity()
                order.calculate_userRate()
                return render(request,'products/showResultOfOrder.html', {'order':order})
            else:
                messages.warning(request, 'اطلاعات وارد شده نامعتبر است!')
                return redirect('products:confirm-order')

        profile_form = Profile_form(instance=request.user.user_info)
        context={
            'order' : order,
            'profile_form' : profile_form
        }

        return render(request, 'products/confirm_order.html', context)

    raise Http404()
    


@login_required(login_url='/')  
def select_delivery(request):
    if request.method=='POST':
        value_select = request.POST['select_delivery_type']
        delivery_instance = Delivery.objects.get(id=value_select)
        order = Order.objects.get(user=request.user, complete=False)
        order.delivery = delivery_instance
        order.save()
    return redirect('products:show-cart')
