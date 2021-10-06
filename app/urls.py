from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.homepage, name='homepage'),
                  path('signup/', views.user_signup, name='signup'),
                  path('login/', views.user_login, name='login'),
                  path('additionaldetails/', views.additional_details, name='additionaldetails'),
                  path('logout/', views.logout_user, name='logout'),
                  path('search/', views.search_items, name='search'),
                  path('search/<int:pk>/', views.search_items, name='search'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
