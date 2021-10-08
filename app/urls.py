from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# app_name = 'app'
urlpatterns = [
                  path('', views.homepage, name='homepage'),
                  path('signup/', views.user_signup, name='signup'),
                  path('login/', views.user_login, name='login'),
                  path('additionaldetails/', views.additional_details, name='additionaldetails'),
                  path('logout/', views.logout_user, name='logout'),
                  path('search/', views.search_items, name='search'),
                  path('product/add-to-cart/<pk>/', views.add_kart, name='add-to-cart'),
                  path('product/remove-from-cart/<pk>/', views.remove_from_kart, name='remove-from-cart'),
                  path('product/increase-cart/<pk>/', views.increase_cart, name='increase-cart'),
                  path('product/decrease-cart/<pk>/', views.decrease_cart, name='decrease-cart'),
                  path('product/cart/', views.open_cart, name='cart'),
                  path('product/checkout/', views.open_checkout, name='checkout'),
                  path('product/<str:slug>/', views.view_product, name='product'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
