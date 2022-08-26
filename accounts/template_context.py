from calendar import c
from products.models import Category
from .models import Slider
from .forms import Custom_userCreationForm, Custom_authentication_form


def show_navbar(request):
        return {'show_navbar': Category.objects.all(),
                'register_form': Custom_userCreationForm(), 
                'login_form':Custom_authentication_form()
            }


def show_slider(request):

    return {'slides' : Slider.objects.all()}


def order_count(request):
    context = {'order_items_count':0}
    if request.user.is_authenticated: 
        unrecorded_order = request.user.order_set.filter(complete=False)
        if unrecorded_order:
            order_items_count = unrecorded_order[0].get_total_quantity()
            context = {'order_items_count':order_items_count}
    return context

def get_user_rate(request):
    if request.user.is_authenticated: 
        return {'user_rate': request.user.rate}  
    return {}


