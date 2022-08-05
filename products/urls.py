from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('category/<str:name>', views.show_products, name = "show-products"),
    path('<int:pk>/', views.detail_product, name = "detail-product"),
    path('search/', views.result_search, name = "search"),
    path('comment/<int:pk>/', views.send_comment, name = "send-comment"),
    path('reply_comment/<int:pk>/', views.send_reply, name = "send-reply"),
    path('liked/<int:pk>/', views.add_likes, name = "add-likes"),
    path('add_order', views.add_order, name = "add-order"),
    path('update_order', views.update_order, name = "update-order"),
    path('show_cart', views.show_cart, name = "show-cart"),
    path('liked_list/', views.show_likes, name = "liked-list"),
    path('about_us/', views.about_us, name = "about-us"),
    path('delete_liked/<int:pk>/', views.delete_liked, name = "delete_liked"),
    path('delete_orderItem/<int:pk>/', views.delete_orderItem, name = "delete_order_item"),
    path('confirm_order/', views.confirm_order, name = "confirm-order"),
    path('select_delivery/', views.select_delivery, name = "select-delivery"),


    
     
]
































