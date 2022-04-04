from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('category/', views.show_category, name = "show-category"),
    path('category/<str:name>', views.show_products, name = "show-products"),
    path('<int:pk>/', views.detail_product, name = "detail-product"),
    path('comment/<int:pk>/', views.send_comment, name = "send-comment"),
    path('liked/<int:pk>/', views.add_likes, name = "add-likes"),
    
   
    
]

