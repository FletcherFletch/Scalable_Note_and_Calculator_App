"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Helper.views import about_view, payment_cancel, delete_note, home_view, login_view, placeholder_view, register_view, create_price, note_display
from users.views import NotesView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notes', NotesView, basename='notes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('Login/', login_view, name='Login'),
    path('user/', placeholder_view, name='user_subscription'),
    path('user2/', placeholder_view, name="account_logout"),
    path('user3/', placeholder_view, name="pricing"),
    path('user5/', placeholder_view, name="account_signup"),
    path('user6/', placeholder_view, name="account_login"),
    path('register/', register_view, name='register'),
  #  path('checkout/<int:django_product_id>/', create_checkout_view, name='checkout'),
    path('price/<int:django_product_id>/', create_price, name="price"),
    path('notes/', payment_cancel, name="display_notes"),
    path('notes/delete/<int:note_id>/', delete_note, name='delete_note'),
    path('', include(router.urls)),
]
